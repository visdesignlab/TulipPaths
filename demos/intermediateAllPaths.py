""" Example of finding paths and visualizing them for debugging. """

from tulip import *
from tulipgui import *
import tulippaths as tp

# Path parameters
graphFile = '../data/test_one.tlp'
sourceNodeId = 176
maxNumHops = 2

# Load the graph
graph = tlp.loadGraph(graphFile)

# Find start and end nodes
source = tp.getNodeById(sourceNodeId, graph)

# Find paths
finder = tp.PathFinder(graph)
results = finder.findAllPaths(source, maxNumHops)

print 'The valid paths are:'
for path in finder.valid:
    print '  ' + path.toString()
    print '  ' + path.toStringOfTypes()
    print '  ' + path.toStringOfIds()

# Make all edges and nodes transparent
transparentGrey = tlp.Color(50, 50, 50, 50)
tp.setEdgeColor(transparentGrey, graph)
tp.setNodeColor(transparentGrey, graph)

# Render the graph in a node-link diagram.
nodeLinkView = tlpgui.createNodeLinkDiagramView(graph)