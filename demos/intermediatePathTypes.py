""" Example of finding paths """

from tulip import *
from tulipgui import *
import TulipPaths as tp

# Load the graph.
graph = tlp.loadGraph("../tests/test_one.tlp")
nodeIds = graph.getProperty("ID")

# Find start and end nodes
startNode = tp.getNodeByID(176, nodeIds, graph)
endNode = tp.getNodeByID(606, nodeIds, graph)

# Find paths
results = tp.findPaths(startNode, endNode, 3, graph)

# Print paths
print 'The failed paths are:'
for path in results['failedPaths']:
    print '  ' + path.toString()

print 'The valid paths are:'
for path in results['validPaths']:
    print '  ' + path.toString()

# Render the graph in a node-link diagram.
nodeLinkView = tlpgui.createNodeLinkDiagramView(graph)