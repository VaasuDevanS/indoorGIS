# Django imports
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.gis.gdal import DataSource

# Project imports
from indoorGIS.settings import STATIC_ROOT as static
from .models import ELevel, DLevel, CLevel, BLevel
from .categories import categorize

# Module imports
from os.path import join
import geopandas as gpd
import networkx as nx

# For reading SHP files
HeadHall = join(static, "HeadHall", "SHPs")
blks = [join(HeadHall, "%s_Level_Blocks" % i) for i in "EDCB"]
lvls = [(ix, "%s Level" % i) for ix, i in enumerate("EDCB")]


# Rounding function for geom coordinates
def rounding(x): return round(x, 4)


# Get name after trimming the level
def name(x): return x.split(":")[1].strip()


# Route Network
RouteLayer = DataSource(join(HeadHall, "E_Level_Route"))[0]
geom = [pt.tuple for pt in RouteLayer.get_geoms()]
edges = []
for g in geom:
    if len(g) == 2:
        edges.append([(rounding(ptX), rounding(ptY)) for ptX, ptY in g])
    else:
        for k in zip(g, g[1:]):
            edges.append([(rounding(ptX), rounding(ptY)) for ptX, ptY in k])

# Build Network Dataset
ND = nx.Graph()
ND.add_edges_from(edges)
ND.add_nodes_from(set([node for edge in edges for node in edge]))

# -----------------------------------------------------------------------------


def home(request):
    return render(request, 'home.html', {})


def loadFields(request):

    allFlds = []
    for k, blkFile in zip(["E-Lvl", "D-Lvl", "C-Lvl", "B-Lvl"], blks):
        blk = gpd.read_file(blkFile)
        fields = set(blk.PlaceName.tolist() + blk.PersonName.tolist())
        fields.remove(None)
        for val in fields:
            allFlds.append({'value': '%s: %s' % (k, val),
                            'label': val})
    return HttpResponse(str(sorted(allFlds, key=lambda x: x["label"])))


def loadCategories(request):

    html = [categorize(blk, *lvl) for blk, lvl in zip(blks, lvls)]
    return HttpResponse("".join(html))


def loadJSON(request):

    JSON = [gpd.read_file(blk).to_json() for blk in blks]
    return HttpResponse(str(JSON))


def create_model_objects(request):

    # Dump Geopandas Blocks to model
    for blkFile, level in zip(blks, [ELevel, DLevel, CLevel, BLevel]):
        blk = gpd.read_file(blkFile)
        blk["geometry"] = blk.geometry.apply(lambda g: g.wkt)
        for rec in blk.to_records(index=False):
            level.objects.update_or_create(**dict(zip(blk.columns, rec)))

    return redirect("/AdminLogin")


def searchBox(request):

    kwrd = name(request.POST["keyword"])
    blksDF = gpd.pd.concat([gpd.read_file(blk) for blk in blks], keys=range(4))
    res = blksDF.query("PlaceName==@kwrd | PersonName==@kwrd")
    return HttpResponse(str([int(res.OBJECTID), int(res.index.codes[0])]))


def from_to_route(request):

    frm, to = name(request.POST["from"]), name(request.POST["to"])
    eBlks = gpd.read_file(join(HeadHall, "E_Level_Blocks"))

    # Get the Placenodes based on PlaceName or PersonName
    frmNode = eBlks.query("PlaceName==@frm | PersonName==@frm").PlaceNode
    toNode = eBlks.query("PlaceName==@to | PersonName==@to").PlaceNode
    return solve_network(int(frmNode), int(toNode))


def solve_network(start, end):

    # Read SHPs
    eBlks = gpd.read_file(join(HeadHall, "E_Level_Blocks"))
    places = gpd.read_file(join(HeadHall, "E_Level_Places"))

    # Get the extent of the selected blocks
    extent = eBlks.query("PlaceNode in [@start, @end]").geometry.total_bounds

    # Get ObjectID for styling
    oIds = eBlks.query("PlaceNode in [@start, @end]").OBJECTID.tolist()

    # Get the Start and End point on the network based on selected blocks
    start = places.geometry[places.PlaceNode == start].tolist()[0]
    end = places.geometry[places.PlaceNode == end].tolist()[0]
    startPt = (float(rounding(start.x)), float(rounding(start.y)))
    endPt = (float(rounding(end.x)), float(rounding(end.y)))

    # Euclidean distance function
    def dist(a, b): return ((a[0]-b[0])**2 + (a[1]-b[1])**2) ** 0.5

    # Solve the network and return the resultant nodes (reversed for leaflet)
    result = [list(i)[::-1] for i in nx.astar_path(ND, startPt, endPt, dist)]
    return HttpResponse("[%s, %s, %s]" % (extent.tolist(), result, oIds))

# EOF
