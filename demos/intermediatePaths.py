""" Example of finding paths """

from tulip import *
from tulipgui import *
import TulipPaths as tp

# Load the graph.
graph = tlp.loadGraph("../tests/test_one.tlp")
nodeIds = graph.getProperty("ID")

# Find start and end nodes
startNode = tp.getNodeByID(176, nodeIds, graph)
endNode = tp.getNodeByID(606, nodeIds, graph)

# Find paths
paths = tp.findPaths(startNode, endNode, 2, graph)

# Print paths
for path in paths:
    pathStr = ''
    for node in path:
        pathStr = pathStr + nodeIds[node] + ', '
    print pathStr

# Render the graph in a node-link diagram.
nodeLinkView = tlpgui.createNodeLinkDiagramView(graph)