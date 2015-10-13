""" Example of finding paths and visualizing them for debugging. """

from tulip import *
from tulipgui import *
import TulipPaths as tp

# Path parameters
graphFile = '../tests/test_one.tlp'
sourceNodeId = 176
targetNodeId = 606
maxNumHops = 4

# We will visualize our second valid path for debugging. This assumes that we'll find at least two paths in the graph.
visualizePathIndex = 2

# Load the graph
graph = tlp.loadGraph(graphFile)

# Find start and end nodes
startNode = tp.getNodeById(sourceNodeId, graph)
endNode = tp.getNodeById(targetNodeId, graph)

# Find paths
results = tp.findPaths(startNode, endNode, maxNumHops, graph)
validPaths = results['validPaths']
failedPaths = results['failedPaths']

# Print paths
print 'The failed paths are:'
for path in failedPaths:
    print '  ' + path.toString()

print 'The valid paths are:'
for path in validPaths:
    print '  ' + path.toString()

# Make all edges and nodes transparent
transparentGrey = tlp.Color(50, 50, 50, 50)
tp.setEdgeColor(transparentGrey, graph)
tp.setNodeColor(transparentGrey, graph)

# Set the desired path to red
assert len(validPaths) > visualizePathIndex, 'Error - visualize path index > num valid paths'
tp.setPathColor(validPaths[visualizePathIndex], tlp.Color.Red, graph)

# Render the graph in a node-link diagram.
nodeLinkView = tlpgui.createNodeLinkDiagramView(graph)