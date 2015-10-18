""" Example of finding paths and visualizing them for debugging. """

from tulip import *
from tulipgui import *
import tulippaths as tp

# Path parameters
graphFile = '../data/514_4hops.tlp'
sourceNodeId = 593
targetNodeId = 514
maxNumHops = 5

# We will visualize our second valid path for debugging. This assumes that we'll find at least two paths in the graph.
visualizePathIndex = 2

# Load the graph
graph = tlp.loadGraph(graphFile)

# Find start and end nodes
startNode = tp.getNodeById(sourceNodeId, graph)
endNode = tp.getNodeById(targetNodeId, graph)

# Find paths
print 'num hops, num valid paths, total paths, num paths with loops back to start, num remaining paths'
visualizePaths = []
uniqueTypes = 0
uniqueTypesCount = 0

for i in range(1, 5):
    results = tp.findPaths(startNode, endNode, i, graph)
    validPaths = results['validPaths']
    failedPaths = results['failedPaths']
    visualizePaths = []
    numPathsWithLoop = 0
    uniqueTypesCount = []
    uniqueTypes = []
    for path in validPaths:
        if path.nodes[0] in path.nodes[1:]:
            numPathsWithLoop += 1
        else:
            visualizePaths.append(path)

        found = False
        for j in range(0, len(uniqueTypes)):
            other = uniqueTypes[j]
            if path.isSameType(other):
                uniqueTypesCount[j] += 1
                found = True
                break

        if not found:
            uniqueTypes.append(path)
            uniqueTypesCount.append(1)

    check = 0
    for j in range(0, len(uniqueTypesCount)):
        check = check + uniqueTypesCount[j]
    assert check==len(validPaths)

    print str(i) + ', ' + str(len(validPaths) + len(failedPaths)) + ', ' + str(len(validPaths)) + ', ' + \
          str(len(validPaths) - numPathsWithLoop) + ', ' + str(len(uniqueTypes))




# Print paths
#print 'The failed paths are:'
#for path in failedPaths:
#    print '  ' + path.toString()

print 'The ' + str(len(uniqueTypes)) + ' valid paths are:'
for path in uniqueTypes:
    print '  ' + path.toString()

for i in range(0, len(uniqueTypes)):
    path = uniqueTypes[i]
    print '  ' + path.toStringOfTypes() + ', ' + str(uniqueTypesCount[i])

# Make all edges and nodes transparent
transparentGrey = tlp.Color(50, 50, 50, 25)
tp.setEdgeColor(transparentGrey, graph)
tp.setNodeColor(transparentGrey, graph)

# Set the desired path to red
assert len(validPaths) > visualizePathIndex, 'Error - visualize path index > num valid paths'
for path in visualizePaths:
    tp.setPathColor(path, tlp.Color.Red, graph)

# Render the graph in a node-link diagram.
nodeLinkView = tlpgui.createNodeLinkDiagramView(graph)