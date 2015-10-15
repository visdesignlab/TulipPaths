""" Example of accessing nodes using the tulip paths utils """
from tulip import *
from tulipgui import *
import TulipPaths as tp

# Load the graph.
graph = tlp.loadGraph("../data/test_one.tlp")

startNode = tp.getNodeById(176, graph)
endNode = tp.getNodeById(606, graph)

print startNode
print endNode

# Render the graph in a node-link diagram.
nodeLinkView = tlpgui.createNodeLinkDiagramView(graph)

