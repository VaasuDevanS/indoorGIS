# Django imports
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.gis.gdal import DataSource

# Project imports
from indoorGIS.settings import STATIC_ROOT as static
from .models import ELevel

# Module imports
import geopandas as gpd
import networkx as nx
import os

# For reading SHP files
HeadHall = os.path.join(static, "HeadHall", "SHPs")

# rounding function for geom coordinates
rounding = lambda i: round(i, 4)

# Route Network
RouteLayer = DataSource(os.path.join(HeadHall, "E_Level_Route"))[0]
geom = [pt.tuple for pt in RouteLayer.get_geoms()]
edges = []
for g in geom:
    if len(g) == 2:
        edges.append([(rounding(ptX),rounding(ptY)) for ptX,ptY in g])
    else:
        for k in zip(g, g[1:]):
            edges.append([(rounding(ptX),rounding(ptY)) for ptX,ptY in k])

# Build Network Dataset
ND = nx.Graph()
ND.add_edges_from(edges)
ND.add_nodes_from(set([node for edge in edges for node in edge]))


def home(request):
    return render(request, 'home.html', {})


def loadFields(request):

    eBlocks = gpd.read_file(os.path.join(HeadHall, "E_Level_Blocks"))
    fields = set(eBlocks.PlaceName.tolist() + eBlocks.PersonName.tolist())
    fields.remove(None)
    return HttpResponse(str(sorted(fields)))


def loadJSON(request):

    eBlocks = gpd.read_file(os.path.join(HeadHall, "E_Level_Blocks"))
    return HttpResponse(eBlocks.to_json())


def create_model_objects(request):

    # Dump Geopandas Blocks to model
    blocks = gpd.read_file(os.path.join(HeadHall, "E_Level_Blocks"))
    blocks["geometry"] = blocks.geometry.apply(lambda g:g.wkt)
    for rec in blocks.to_records(index=False):
        ELevel.objects.update_or_create(**dict(zip(blocks.columns, rec)))
    return redirect("/AdminLogin")


def searchBox(request):

    kwrd = request.POST["keyword"]
    eBlks = gpd.read_file(os.path.join(HeadHall, "E_Level_Blocks"))

    searchID = eBlks.query("PlaceName==@kwrd | PersonName==@kwrd").OBJECTID
    return HttpResponse(str(int(searchID)))


def from_to_route(request):

    frm, to = request.POST["from"], request.POST["to"]
    eBlks = gpd.read_file(os.path.join(HeadHall, "E_Level_Blocks"))

    frmNode = eBlks.query("PlaceName==@frm | PersonName==@frm").PlaceNode
    toNode = eBlks.query("PlaceName==@to | PersonName==@to").PlaceNode

    return solve_network(request, int(frmNode), int(toNode))


def solve_network(request, start=None, end=None):

    # Read SHPs
    eBlks = gpd.read_file(os.path.join(HeadHall, "E_Level_Blocks"))
    places = gpd.read_file(os.path.join(HeadHall, "E_Level_Places"))

    if start == None:
        start, end = int(request.POST["from"]), int(request.POST["to"])

    # Get the extent of the selected blocks
    extent = eBlks.query("PlaceNode in [@start, @end]").geometry.total_bounds

    # Get ObjectID for styling
    oIds = eBlks.query("PlaceNode in [@start, @end]").OBJECTID.tolist()

    # Get the Start and End point on the network based on selected blocks
    start = places.geometry[ places.PlaceNode==start ].tolist()[0]
    end = places.geometry[ places.PlaceNode==end ].tolist()[0]
    startPt = (float(rounding(start.x)), float(rounding(start.y)))
    endPt = (float(rounding(end.x)), float(rounding(end.y)))

    # Euclidean distance function
    dist = lambda a,b: ((a[0]-b[0])**2 + (a[1]-b[1])**2) ** 0.5

    # Solve the network and return the resultant nodes (reversed for leaflet)
    result = [list(i)[::-1] for i in nx.astar_path(ND, startPt, endPt, dist)]
    return HttpResponse("[%s, %s, %s]" % (extent.tolist(), result, oIds))

# EOF