""" Example of finding paths and visualizing them for debugging. """

from tulip import *
from tulipgui import *
import tulippaths as tp

# Path parameters
graphFile = '../data/test_three.tlp'
sourceNodeId = 1724
targetNodeType = 'GC'
maxNumHops = 4

# Load the graph and find nodes of interest.
graph = tlp.loadGraph(graphFile)
sourceNode = tp.utils.getNodeById(sourceNodeId, graph)
targetNodes = tp.utils.getNodesByType(targetNodeType, graph)

validPaths = []
failedPaths = []
for target in targetNodes:
    results = tp.pathFinder(sourceNode, target, maxNumHops, graph)
    results = results['validPaths']
    for path in results:
        validPaths.append(path)

for path in validPaths:
    print path.toString()

# Make all edges and nodes transparent
transparentGrey = tlp.Color(50, 50, 50, 50)
tp.setEdgeColor(transparentGrey, graph)
tp.setNodeColor(transparentGrey, graph)

# Set the desired path to red
#assert len(validPaths) > visualizePathIndex, 'Error - visualize path index > num valid paths'
#tp.setPathColor(validPaths[visualizePathIndex], tlp.Color.Red, graph)

# Render the graph in a node-link diagram.
nodeLinkView = tlpgui.createNodeLinkDiagramView(graph)