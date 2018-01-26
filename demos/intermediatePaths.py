""" Example of finding paths and visualizing them for debugging. """

from tulip import *
from tulipgui import *
import tulippaths as tp

# Path parameters
graphFile = '../data/test_one.tlp'
sourceNodeId = 176
targetNodeId = 606
maxNumHops = 4

# We will visualize our second valid path for debugging. This assumes that we'll find at least two paths in the graph.
visualizePathIndex = 2

# Load the graph
graph = tlp.loadGraph(graphFile)

# Find start and end nodes
source = tp.getNodeById(sourceNodeId, graph)
target = tp.getNodeById(targetNodeId, graph)

# Find paths
finder = tp.PathFinder(graph)
results = finder.findPaths(source, target, maxNumHops)

# Print paths
print('The failed paths are:')
for path in finder.failed:
    print(('  ' + path.toString()))

print('The valid paths are:')
for path in finder.valid:
    print(('  ' + path.toString()))

# Make all edges and nodes transparent
transparentGrey = tlp.Color(50, 50, 50, 50)
tp.setEdgeColor(transparentGrey, graph)
tp.setNodeColor(transparentGrey, graph)

# Set the desired path to red
assert len(finder.valid) > visualizePathIndex, 'Error - visualize path index > num valid paths'
tp.setPathColor(finder.valid[visualizePathIndex], tlp.Color.Red, graph)

# Render the graph in a node-link diagram.
nodeLinkView = tlpgui.createNodeLinkDiagramView(graph)