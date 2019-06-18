from indoorGIS.settings import STATIC_ROOT as static
from django.shortcuts import render, HttpResponse
from django.contrib.gis.gdal import DataSource
import geopandas as gpd
import networkx as nx
import os

def home(request):
    return render(request, 'home.html', {})

# Route solver
def solve_network(request):

    start, end = int(request.POST["from"]), int(request.POST["to"])
    HeadHall = os.path.join(static, "HeadHall", "SHPs")

    # Read Blocks and Places SHP files
    blocks = gpd.read_file(os.path.join(HeadHall, "E_Level_Blocks"))
    places = gpd.read_file(os.path.join(HeadHall, "E_Level_Places"))
    RouteLayer = DataSource(os.path.join(HeadHall, "E_Level_Route"))[0]

    # Get the extent of the selected blocks
    extent = blocks.query("PlaceNode in %s"%[start,end]).geometry.total_bounds

    # Get the Start and End point on the network based on selected blocks
    start = places.geometry[ places.PlaceNode==start ].tolist()[0]
    end = places.geometry[ places.PlaceNode==end ].tolist()[0]
    startPt = (float(round(start.x,4)), float(round(start.y,4)))
    endPt = (float(round(end.x,4)), float(round(end.y,4)))

    # Build the Route Network
    geom = [pt.tuple for pt in RouteLayer.get_geoms()]
    edges = []
    for g in geom:
        if len(g) == 2:
            edges.append([(round(ptX,4),round(ptY,4)) for ptX,ptY in g])
        else:
            for k in zip(g, g[1:]):
                edges.append([(round(ptX,4),round(ptY,4)) for ptX,ptY in k])

    # Build Network Dataset
    ND = nx.Graph()
    ND.add_nodes_from(set([j for i in edges for j in i]))
    ND.add_edges_from(edges)

    # Euclidean distance function
    dist = lambda a,b: ((a[0]-a[1])**2 + (b[0]-b[1])**2) ** 0.5

    # Solve the network and return the resultant nodes (reversed for leaflet)
    result = [list(i)[::-1] for i in nx.astar_path(ND, startPt, endPt, dist)]
    return HttpResponse("[%s, %s]" % (extent.tolist(), result))

# EOF