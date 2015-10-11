""" Example of accessing nodes using the tulip paths utils """
from tulip import *
from tulipgui import *
import TulipPaths as tp

# Load the graph.
graph = tlp.loadGraph("../tests/test_one.tlp")

# Initialize array of node properties.
nodeIds = graph.getProperty("ID")

startNode = tp.getNodeByID(176, nodeIds, graph)
endNode = tp.getNodeByID(606, nodeIds, graph)

print startNode
print endNode

# Render the graph in a node-link diagram.
nodeLinkView = tlpgui.createNodeLinkDiagramView(graph)

