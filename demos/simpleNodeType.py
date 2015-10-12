""" Example of accessing nodes using the tulip paths utils """
from tulip import *
from tulipgui import *
import TulipPaths as tp

# Load the graph.
graph = tlp.loadGraph("../tests/test_one.tlp")

for node in graph.getNodes():
    print 'node: ' + str(node) + ' has id ' + str(tp.getNodeId(node, graph)) + ' and type ' + str(tp.getNodeType(node, graph))

for edge in graph.getEdges():
    print tp.getEdgeType(edge, graph)

# Render the graph in a node-link diagram.
nodeLinkView = tlpgui.createNodeLinkDiagramView(graph)