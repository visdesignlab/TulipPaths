""" Example of finding paths and unique types using PathStats """

from tulip import *
from tulipgui import *
import tulippaths as tp

# Path parameters
graphFile = '../data/514_4hops.tlp'
sourceNodeId = 593
targetNodeId = 514
maxNumHops = 5

graph = tlp.loadGraph(graphFile)

# Find start and end nodes
source = tp.getNodeById(sourceNodeId, graph)
target = tp.getNodeById(targetNodeId, graph)

finder = tp.PathFinder(graph)
print 'hops, total, valid, unique, num w\ loop'
for i in range(0, maxNumHops):
    finder.reset()
    finder.findPaths(source, target, i)
    stats = tp.PathStats(finder.valid)

    print str(i) + ', ' + str(len(finder.valid) + len(finder.failed)) + ', ' + str(len(finder.valid)) + ', ' + \
          str(stats.getNumUniqueTypes()) + ', ' + str(stats.getNumPathsWithLoop())

# Render the graph in a node-link diagram.
nodeLinkView = tlpgui.createNodeLinkDiagramView(graph)