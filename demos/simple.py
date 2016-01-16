""" Example of loading graphs in python """

from tulip import *
from tulipgui import *

# Load the graph.
graph = tlp.loadGraph("../data/test_one.tlp")

# Render the graph in a node-link diagram.
nodeLinkView = tlpgui.createNodeLinkDiagramView(graph)