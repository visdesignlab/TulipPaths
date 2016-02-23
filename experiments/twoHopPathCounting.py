__author__ = 'Dasha'

from tulip import *
import tulippaths as tp
import json

# Path parameters
graphFile = '../data/514_10hops_22Jan16.tlp'
#sourceNodeId = 593
sourceNodeId = 485
maxNumHops = 2


# We will visualize our second valid path for debugging. This assumes that we'll find at least two paths in the graph.
visualizePathIndex = 2

# Load the graph
graph = tlp.loadGraph(graphFile)

pathPrinter = tp.PathPrinter(graph)
pathPrinter.printToFile(sourceNodeId, "../data/jsonTestFile.json")

# Find start and end nodes
source = tp.getNodeById(sourceNodeId, graph)
#target = tp.getNodeById(targetNodeId, graph)

# Find paths
pathFinder = tp.PathFinder(graph)
results = pathFinder.findAllPaths(source, maxNumHops)

uniqueNodeAndEdgeTypeDict = {}
uniqueNodeAndEdgeTypes = []
uniqueNodeAndEdgeTypesCount = []
uniqueNodeTypeDict = {}
uniqueNodeTypes = []
uniqueNodeTypesCount = []
uniqueSuperTypes = []
uniqueSuperTypesCount = []
numNonSynaptic = 0
numValid = 0
numInNetwork = 0
numNonSynapticAndInNetwork = 0

# print 'The valid paths are:'
for path in pathFinder.valid:
    nonSynaptic = False
    inNetwork = False

    if not path.isSynapticPath():
        numNonSynaptic += 1
        nonSynaptic = True

    if path.isInNetworkPath():
        numInNetwork += 1
        inNetwork = True

    if nonSynaptic and inNetwork:
        numNonSynapticAndInNetwork += 1

    # We want to ignore paths that are not synaptic or are in network
    if nonSynaptic or inNetwork:
        continue

    # print '  ' + path.toStringOfTypes()

    numValid += 1

    found = False
    for j in range(0, len(uniqueNodeAndEdgeTypes)):
        other = uniqueNodeAndEdgeTypes[j]
        if path.isSameType(other):
            uniqueNodeAndEdgeTypesCount[j] += 1
            found = True
            break

    if not found:
        uniqueNodeTypes.append(path)
        uniqueNodeTypesCount.append(1)

    found = False
    for j in range(0, len(uniqueNodeTypes)):
        other = uniqueNodeTypes[j]
        if path.isSameNodeType(other):
            uniqueNodeTypesCount[j] += 1
            found = True
            break

    if not found:
        uniqueNodeTypes.append(path)
        uniqueNodeTypesCount.append(1)

    # Same thing for super types
    found = False
    for j in range(0, len(uniqueSuperTypes)):
        other = uniqueSuperTypes[j]
        if path.isSameSuperType(other):
            uniqueSuperTypesCount[j] += 1
            found = True
            break

    if not found:
        uniqueSuperTypes.append(path)
        uniqueSuperTypesCount.append(1)

mostCommonPath = uniqueNodeTypes[0]
pathFrequency = uniqueNodeTypesCount[0]
hammingDistanceHistogram = [0, 0, 0, 0, 0, 0]

print "Types"
for i in range (0, len(uniqueNodeTypesCount)):
    print str(uniqueNodeTypesCount[i]) + "\t" + str(uniqueNodeTypes[i].toStringOfTypes())
    if(pathFrequency < uniqueNodeTypesCount[i]):
        pathFrequency = uniqueNodeTypesCount[i]
        mostCommonPath = uniqueNodeTypes[i]

mostCommonSuperPath = uniqueSuperTypes[0]
superPathFrequency = uniqueSuperTypesCount[0]
hammingDistanceSuperHistogram = [0, 0, 0, 0, 0, 0]

for i in range (0, len(uniqueSuperTypesCount)):
    # print str(uniqueTypesCount[i]) + "\t" + str(uniqueTypes[i].toStringOfTypes())
    if(superPathFrequency < uniqueSuperTypesCount[i]):
        superPathFrequency = uniqueSuperTypesCount[i]
        mostCommonSuperPath = uniqueSuperTypes[i]

print "Super Types"
for i in range (0, len(uniqueSuperTypesCount)):
    print str(uniqueSuperTypesCount[i]) + "\t" + str(uniqueSuperTypes[i].toStringOfSuperTypes())

print "\nMost common path is " + str(mostCommonPath.toStringOfTypes())
print "Distances from other paths:"

print "\nHamming Distance\tFrequency\tPath"

for i in range (0, len(uniqueNodeTypesCount)):
    toPrint = ""
    # for j in range (0, len(uniqueTypesCount)):
        # toPrint += str(uniqueTypes[i].getDistanceFromOtherPath(uniqueTypes[j])) + "\t"
    # print toPrint
    print str(mostCommonPath.getDistanceFromOtherPath(uniqueNodeTypes[i])) + "\t" + str(uniqueNodeTypesCount[i]) + "\t" + str(uniqueNodeTypes[i].toStringOfTypes())
    hammingDistanceHistogram[mostCommonPath.getDistanceFromOtherPath(uniqueNodeTypes[i])] += uniqueNodeTypesCount[i]


print "Hamming Distance\tFrequency"

for i in range (0, len(hammingDistanceHistogram)):
    print str(i) + "\t" + str(hammingDistanceHistogram[i])

print "********************"
print "Super types"
print "\nHamming Distance\tFrequency\tPath"
for i in range (0, len(uniqueSuperTypesCount)):
    toPrint = ""
    # for j in range (0, len(uniqueTypesCount)):
        # toPrint += str(uniqueTypes[i].getDistanceFromOtherPath(uniqueTypes[j])) + "\t"
    # print toPrint
    print str(mostCommonSuperPath.getSuperDistanceFromOtherPath(uniqueSuperTypes[i])) + "\t" + str(uniqueSuperTypesCount[i]) + "\t" + str(uniqueSuperTypes[i].toStringOfNodeTypes())
    hammingDistanceSuperHistogram[mostCommonSuperPath.getSuperDistanceFromOtherPath(uniqueSuperTypes[i])] += uniqueSuperTypesCount[i]


print "Hamming Distance\tFrequency"

for i in range (0, len(hammingDistanceSuperHistogram)):
    print str(i) + "\t" + str(hammingDistanceSuperHistogram[i])


print '\n' + str(numValid) + " total " + str(maxNumHops) + "-hop synaptic paths from node #" + str(sourceNodeId)

print '\n' + str(len(uniqueNodeTypesCount)) + " unique path types"

print '\n' + str(len(uniqueSuperTypesCount)) + " unique path super types"

print '\n' + str(numNonSynaptic) + " non-synaptic paths were ignored, " + str(numInNetwork) + \
      " in-network paths were ignored; " + str(numNonSynapticAndInNetwork) + " were both."

print '\n' + str(sourceNodeId) + '\t' + str(numValid) + '\t' + str(len(uniqueNodeTypesCount)) + '\t' + \
      str(len(uniqueSuperTypesCount)) + '\t' + str(numNonSynaptic) + '\t' + str(numInNetwork) + '\t' + str(numNonSynapticAndInNetwork)

#Map super node types -> node types -> node edge types
