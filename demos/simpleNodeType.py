""" Example of accessing node and edge types using the tulip paths utils """
from tulip import *
from tulipgui import *
import TulipPaths as tp

# Load the graph.
graph = tlp.loadGraph("../tests/test_one.tlp")

print 'The nodes:'
for node in graph.getNodes():
    print 'node: ' + str(node) + ' has id ' + str(tp.getNodeId(node, graph)) +  \
          ' and type ' + str(tp.getNodeType(node, graph))

print 'The edges'
for edge in graph.getEdges():
    print 'edge: ' + str(edge) + ' has type ' + tp.getEdgeType(edge, graph)

# Render the graph in a node-link diagram.
nodeLinkView = tlpgui.createNodeLinkDiagramView(graph)