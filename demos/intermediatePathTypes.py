""" Example of finding paths and printing type details. """

from tulip import *
from tulipgui import *
import tulippaths as tp

# Load the graph.
graph = tlp.loadGraph("../data/test_one.tlp")

# Find start and end nodes
source = tp.getNodeById(176, graph)
target = tp.getNodeById(606, graph)

# Find paths
finder = tp.PathFinder(graph)
finder.findPaths(source, target, 3)

# Print paths
print 'The failed paths are:'
for path in finder.valid:
    print '  ' + path.toString()

print 'The valid paths are:'
for path in finder.valid:
    print '  ' + path.toString()

print 'The valid paths types are:'
for path in finder.valid:
    print '  ' + path.toStringOfTypes()

# Render the graph in a node-link diagram.
nodeLinkView = tlpgui.createNodeLinkDiagramView(graph)