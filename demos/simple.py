""" Example of loading graphs in python """

from tulip import *
from tulipgui import *

# Load the graph.
graph = tlp.loadGraph("../tests/test_three.tlp")

# Render the graph in a node-link diagram.
nodeLinkView = tlpgui.createNodeLinkDiagramView(graph)