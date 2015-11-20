""" Example of finding paths and visualizing them for debugging. """

from tulip import *
from tulipgui import *
import tulippaths as tp

# Path parameters
graphFile = '../data/514_4hops.tlp'
#sourceNodeId = 593
sourceNodeId = 593
targetNodeId = 514
maxNumHops = 5

# We will visualize our second valid path for debugging. This assumes that we'll find at least two paths in the graph.
visualizePathIndex = 2

# Load the graph
graph = tlp.loadGraph(graphFile)

# Find start and end nodes
source = tp.getNodeById(sourceNodeId, graph)
target = tp.getNodeById(targetNodeId, graph)

# Find paths
print 'num hops, num valid paths, total paths, num paths with loops back to start, num remaining paths'
visualizePaths = []
binTotalPaths = {}
binPathTypes = {}
uniqueTypes = 0
uniqueTypesCount = 0

finder = tp.PathFinder(graph)
for i in range(1, 5):
    finder.reset()
    finder.findPaths(source, target, i)
    visualizePaths = []
    numPathsWithLoop = 0
    uniqueTypesCount = []
    uniqueTypes = []
    for path in finder.valid:
        if path.nodes[0] in path.nodes[1:]:
            numPathsWithLoop += 1
        else:
            visualizePaths.append(path)

        # Bin paths by first edge
        pathType = tp.getEdgeType(path.edges[0], graph)
        if pathType in binTotalPaths:
            binTotalPaths[pathType] += 1
        else:
            binTotalPaths[pathType] = 1

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
    assert check==len(finder.valid)

    print str(i) + ', ' + str(len(finder.valid) + len(finder.failed)) + ', ' + str(len(finder.valid)) + ', ' + \
          str(len(finder.valid) - numPathsWithLoop) + ', ' + str(len(uniqueTypes))

print "Printing unique types counts:"
for count in uniqueTypesCount:
   print str(count)



print 'The ' + str(len(uniqueTypes)) + ' valid paths are:'
for path in uniqueTypes:
    #print '  ' + path.toString()
    pathType = tp.getEdgeType(path.edges[0], graph)
    if pathType in binPathTypes:
        binPathTypes[pathType] += 1
    else:
        binPathTypes[pathType] = 1


print "For each path type, the relative counts are: "
for startingCount in binPathTypes:
    print str(startingCount) + "\t" + str(binPathTypes[startingCount])

print "For each path, the relative counts are: "
for startingCount in binTotalPaths:
    print str(startingCount) + "\t" + str(binTotalPaths[startingCount])

print "The edge weights for each path are: "
for path in uniqueTypes:
   print "",
   for edge in path.edges:
       print str(tp.getEdgeWeight(edge, graph)) + "\t",
   print ""

print "Percentage of paths that have a loop: " + str(numPathsWithLoop) + "/" + str(len(visualizePaths)) + " = " + str((numPathsWithLoop/len(visualizePaths)))

#for i in range(0, len(uniqueTypes)):
#    path = uniqueTypes[i]
#    print '  ' + path.toStringOfTypes() + ', ' + str(uniqueTypesCount[i])

# Make all edges and nodes transparent
transparentGrey = tlp.Color(50, 50, 50, 25)
tp.setEdgeColor(transparentGrey, graph)
tp.setNodeColor(transparentGrey, graph)

# Set the desired path to red
assert len(finder.valid) > visualizePathIndex, 'Error - visualize path index > num valid paths'
#for path in visualizePaths:
#    tp.setPathColor(path, tlp.Color.Red, graph)

# Render the graph in a node-link diagram.
#nodeLinkView = tlpgui.createNodeLinkDiagramView(graph)