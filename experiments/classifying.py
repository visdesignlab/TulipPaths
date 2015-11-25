""" Example of finding paths and visualizing them for debugging. """

from tulip import *
from tulipgui import *
import tulippaths as tp

# Path parameters
graphFile = '../data/514_10hops.tlp'
sourceNodeId = 593
maxNumHops = 2

# Load the graph
graph = tlp.loadGraph(graphFile)

# Find start and end nodes
sources = tp.getNodesByType('CBb5w', graph)
sources += tp.getNodesByType('CBb4w', graph)
#sources = tp.getNodesByType('CBb3m', graph)

# Make all edges and nodes transparent
transparentGrey = tlp.Color(50, 50, 50, 0)
tp.setEdgeColor(transparentGrey, graph)
tp.setNodeColor(transparentGrey, graph)

# Find paths
tracker = tp.PathTracker()
pathCountDictionary = {}
pathsPerNodeCountDictionary = {}
for source in sources:
    finder = tp.PathFinder(graph)
    results = finder.findAllPaths(source, maxNumHops)

    #print 'The valid paths are:'
    #for path in finder.valid:
       # print ' ' + path.toStringOfTypes()

    red = tlp.Color(255, 0, 0, 255)
    pathsPerNodeCountDictionary[source] = {}
    for path in finder.valid:
        tp.setPathColor(path, red, graph)
        pathId = tracker.getOrCreatePathTypeID(path)

        if pathCountDictionary.has_key(pathId):
            pathCountDictionary[pathId] += 1
        else:
            pathCountDictionary[pathId] = 1

        if pathsPerNodeCountDictionary[source].has_key(pathId):
            pathsPerNodeCountDictionary[source][pathId] += 1
        else:
            pathsPerNodeCountDictionary[source][pathId] = 1


assert(len(pathCountDictionary.keys()) == tracker.getNumUniquePathTypes())
numPaths = 0
print pathCountDictionary
for key in pathCountDictionary.keys():
    numPaths += pathCountDictionary[key]


for source in sources:
    sourcePaths = ''
    for i in range(0, tracker.getNumUniquePathTypes()):
        if pathsPerNodeCountDictionary[source].has_key(i):
            sourcePaths += str(pathsPerNodeCountDictionary[source][i]) + ', '
        else:
            sourcePaths += '0, '
    print str(source) +', ' +  tp.getNodeType(source, graph) + ', ' + sourcePaths
print numPaths
print tracker.getNumUniquePathTypes()


# Render the graph in a node-link diagram.
nodeLinkView = tlpgui.createNodeLinkDiagramView(graph)