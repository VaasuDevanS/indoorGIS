# Django imports
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.gis.gdal import DataSource

# Project imports
from indoorGIS.settings import STATIC_ROOT as static
from .models import ELevel, DLevel, CLevel, BLevel, Stat
from .categories import categorize

# Module imports
from os.path import join
import geopandas as gpd
import networkx as nx


# Rounding function for geom coordinates
def rounding(x): return round(x, 4)


# Get name after trimming the level
def name(x): return x.split(":")[1].strip()


# Get level-code from the name
def level(x): return {"E": 0, "D": 1, "C": 2, "B": 3}[x[0]]


# Euclidean distance function
def dist(a, b): return ((a[0]-b[0])**2 + (a[1]-b[1])**2) ** 0.5


# For reading SHP files
HeadHall = join(static, "HeadHall", "SHPs")
blks = [join(HeadHall, "%s_Level_Blocks" % i) for i in "EDCB"]
routes = [join(HeadHall, "%s_Level_Route" % i) for i in "EDCB"]
places = [join(HeadHall, "%s_Level_Places" % i) for i in "EDCB"]

# Route Network Dataset
ND = {}
for ix, route in enumerate(routes):
    RouteLayer = DataSource(route)[0]
    geom = [pt.tuple for pt in RouteLayer.get_geoms()]
    edges = []
    for g in geom:
        if len(g) == 2:
            edges.append([(rounding(ptX), rounding(ptY)) for ptX, ptY in g])
        else:
            for k in zip(g, g[1:]):
                edges.append([(rounding(ptX), rounding(ptY)) for ptX, ptY in k])

    # Build Network Dataset
    ND[ix] = nx.Graph()
    ND[ix].add_edges_from(edges)
    ND[ix].add_nodes_from(set([node for edge in edges for node in edge]))

# Places DataFrame
placesDF = {ix: gpd.read_file(place) for ix, place in enumerate(places)}

# -----------------------------------------------------------------------------


def home(request):
    return render(request, 'home.html', {})


def loadFields(request):

    allFlds = []
    for k, blkFile in zip(["E-Lvl", "D-Lvl", "C-Lvl", "B-Lvl"], blks):
        blk = gpd.read_file(blkFile)
        fields = set(blk.PlaceName.tolist() +
                     blk.PersonName.tolist() +
                     blk.PlaceNode.astype(str).tolist()
                     )
        fields.remove(None)
        for val in fields:
            allFlds.append({'value': '%s: %s' % (k, val),
                            'label': val})
    return HttpResponse(str(sorted(allFlds, key=lambda x: x["label"])))


def loadCategories(request):

    lvls = [(ix, "%s Level" % i) for ix, i in enumerate("EDCB")]
    html = [categorize(blk, *lvl) for blk, lvl in zip(blks, lvls)]
    return HttpResponse("".join(html))


def loadJSON(request):

    JSON = [gpd.read_file(blk).to_json() for blk in blks]
    return HttpResponse(str(JSON))


def create_model_objects(request):

    # Dump Geopandas Blocks to model
    for blkFile, level_model in zip(blks, [ELevel, DLevel, CLevel, BLevel]):
        blk = gpd.read_file(blkFile)
        blk["geometry"] = blk.geometry.apply(lambda g: g.wkt)
        for rec in blk.to_records(index=False):
            level_model.objects.update_or_create(**dict(zip(blk.columns, rec)))

    return redirect("/AdminLogin")


def searchBox(request):

    # Build BlksDF dictionary
    blksDF = {ix: gpd.read_file(blk) for ix, blk in enumerate(blks)}
    rqst = request.POST

    # Query for the keyword
    kwrd, lvlCode = name(rqst["keyword"]), level(rqst["keyword"])
    res = blksDF[lvlCode].query("PlaceName==@kwrd | PersonName==@kwrd | PlaceNode==@kwrd")

    # Log to Stat model
    Stat.objects.create(functionality="Search",
                        keyword=request.POST["keyword"],
                        returned=True)

    fac = [nearest_facility(lvlCode, int(res.PlaceNode), "Facility,male"),
           nearest_facility(lvlCode, int(res.PlaceNode), "Facility,female"),
           nearest_facility(lvlCode, int(res.PlaceNode), "Steps"),
           nearest_facility(lvlCode, int(res.PlaceNode), "Lift")]

    return HttpResponse(str([int(res.OBJECTID), lvlCode, fac]))


def from_to_route(request):

    rqst = request.POST
    via = rqst["mode"]
    frm, to = name(rqst["from"]), name(rqst["to"])
    frmLvl, toLvl = level(rqst["from"]), level(rqst["to"])
    blksDF = {ix: gpd.read_file(blk) for ix, blk in enumerate(blks)}

    if frmLvl == toLvl:

        blk = blksDF[frmLvl]

        # Get start and end PlaceNode
        start = int(blk.query("PlaceName==@frm | PersonName==@frm | PlaceNode==@frm").PlaceNode)
        end = int(blk.query("PlaceName==@to | PersonName==@to | PlaceNode==@to").PlaceNode)

        # Get the extent of the selected blocks
        extent = blk.query("PlaceNode in [@start, @end]").geometry.total_bounds

        # Get ObjectID for styling
        oIds = blk.query("PlaceNode in [@start, @end]").OBJECTID.tolist()

        try:
            result = solve_network(start, end, frmLvl)
            return_result = str([0, [extent.tolist(), result, oIds, frmLvl]])
            status = True
        except:
            status = False
            return_result = None

    else:

        # origin to via
        blk = blksDF[frmLvl]
        start = int(blk.query("PlaceName==@frm | PersonName==@frm | PlaceNode==@frm").PlaceNode)

        # networkx result
        via_nearest_OID = nearest_facility(frmLvl, start, via)
        via_nearest_node = int(blk.query("PlaceNode==@via_nearest_OID").PlaceNode)
        via_nearest_name = blk.query("PlaceNode==@via_nearest_OID").PlaceName.tolist()[0]
        result = solve_network(start, via_nearest_node, frmLvl)

        # Extent and OIDs
        extent = blk.query("PlaceNode in [@start, @via_nearest_node]").geometry.total_bounds
        oIds = blk.query("PlaceNode in [@start, @via_nearest_node]").OBJECTID.tolist()

        # from level result
        from_level_result = [extent.tolist(), result, oIds, frmLvl]

        # ------------------------------------------------------------------

        # via to destination
        blk = blksDF[toLvl]
        to = int(blk.query("PlaceName==@to | PersonName==@to | PlaceNode==@to").PlaceNode)

        # networkx result
        to_nearest_node = int(blk.query("PlaceName==@via_nearest_name").PlaceNode)
        result = solve_network(to_nearest_node, to, toLvl)

        # Extent and OIDs
        extent = blk.query("PlaceNode in [@to_nearest_node, @to]").geometry.total_bounds
        oIds = blk.query("PlaceNode in [@to_nearest_node, @to]").OBJECTID.tolist()

        # to level result
        to_level_result = [extent.tolist(), result, oIds, toLvl]

        return_result = str([1, from_level_result, to_level_result])
        status = True


    kwrd = "%s to %s via %s" % (rqst["from"], rqst["to"], rqst["mode"])
    Stat.objects.create(functionality="Routing", keyword=kwrd, returned=status)
    return HttpResponse(return_result)


def get_coor(places, pn):

    # Return coordinates in networkx node format
    coor = places.geometry[places.PlaceNode == pn].tolist()[0]
    return (float(rounding(coor.x)), float(rounding(coor.y)))


def solve_network(start, end, lvlCode):

    # Acquire level specific DataFrames for places and ND
    places = placesDF[lvlCode]
    _ND = ND[lvlCode]

    # Get the Start and End point on the network based on selected blocks
    startPt, endPt = get_coor(places, start), get_coor(places, end)

    # Solve the network and return the resultant nodes (reversed for leaflet)
    result = [list(i)[::-1] for i in nx.astar_path(_ND, startPt, endPt, dist)]
    return result


def nearest_facility(lvlCode, frmOID, f):

    blksDF = {ix: gpd.read_file(blk) for ix, blk in enumerate(blks)}
    blk = blksDF[lvlCode]
    places = placesDF[lvlCode]
    _ND = ND[lvlCode]

    cond1 = blk.PlaceName.str.startswith(f, na=False)
    cond2 = blk.PlaceType.str.startswith(f, na=False)

    result = blk[cond1 | cond2]
    res_nodes = result.PlaceNode.tolist()
    res_coords = [get_coor(places, node) for node in res_nodes]

    start = get_coor(places, frmOID)

    pt_distance = {}
    for pn, pt in zip(res_nodes, res_coords):
        pt_distance[pn] = nx.astar_path_length(_ND, start, pt, dist)

    shortest_pnode = sorted(pt_distance, key=lambda x: pt_distance[x])[0]
    return int(result.query("PlaceNode==@shortest_pnode").OBJECTID)

# EOF
