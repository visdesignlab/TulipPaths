""" Example of messing with node color
 This will turn all nodes black, then set the start node and end node to green and red repsectively.
"""
from tulip import *
from tulipgui import *
import tulippaths as tp

graph = tlp.loadGraph("../data/test_one.tlp")

viewColor = graph.getColorProperty("viewColor")

source = tp.getNodeById(176, graph)
target = tp.getNodeById(606, graph)

# Make all nodes black
for node in graph.getNodes():
    viewColor[node] = tlp.Color.Black

# Make start node green and end node red.
viewColor[source] = tlp.Color(0, 255, 0)
viewColor[target] = tlp.Color(255, 0, 0)

# Render the graph in a node-link diagram.
nodeLinkView = tlpgui.createNodeLinkDiagramView(graph)
renderingParameters = nodeLinkView.getRenderingParameters()