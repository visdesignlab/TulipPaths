__author__ = 'Dasha'

"""
For a few different CBb cells, how many 2-hop synaptic paths are there leaving each cell?
How many of these are unique?
What's the distribution of unique path types?  (Does it follow the same long-tail pattern as the 4-hop paths?)
How can we aggregate the unique path types based on the distribution?
     For instance, do the frequently occurring path types have something in common?
How can we aggregate the unique path types based on a distance metric? Something like hamming distance or Levenshtein distance.
How can we aggregate unique path types based on their ending node type?
How can we aggregate the paths using the super-types?
 """

from tulip import *
from tulipgui import *
import tulippaths as tp

# Path parameters
graphFile = '../data/514_10hops_22Jan16.tlp'
#sourceNodeId = 593
sourceNodeId = 483
maxNumHops = 2

# We will visualize our second valid path for debugging. This assumes that we'll find at least two paths in the graph.
visualizePathIndex = 2

# Load the graph
graph = tlp.loadGraph(graphFile)

# Find start and end nodes
source = tp.getNodeById(sourceNodeId, graph)
#target = tp.getNodeById(targetNodeId, graph)

# Find paths
pathFinder = tp.PathFinder(graph)
results = pathFinder.findAllPaths(source, maxNumHops)


uniqueTypes = []
uniqueTypesCount = []
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
    for j in range(0, len(uniqueTypes)):
        other = uniqueTypes[j]
        if path.isSameType(other):
            uniqueTypesCount[j] += 1
            found = True
            break

    if not found:
        uniqueTypes.append(path)
        uniqueTypesCount.append(1)

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

mostCommonPath = uniqueTypes[0]
pathFrequency = uniqueTypesCount[0]
hammingDistanceHistogram = [0, 0, 0, 0, 0, 0]

# print "Types"
for i in range (0, len(uniqueTypesCount)):
    print str(uniqueTypesCount[i]) + "\t" + str(uniqueTypes[i].toStringOfTypes())
    if(pathFrequency < uniqueTypesCount[i]):
        pathFrequency = uniqueTypesCount[i]
        mostCommonPath = uniqueTypes[i]

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

for i in range (0, len(uniqueTypesCount)):
    toPrint = ""
    # for j in range (0, len(uniqueTypesCount)):
        # toPrint += str(uniqueTypes[i].getDistanceFromOtherPath(uniqueTypes[j])) + "\t"
    # print toPrint
    print str(mostCommonPath.getDistanceFromOtherPath(uniqueTypes[i])) + "\t" + str(uniqueTypesCount[i]) + "\t" + str(uniqueTypes[i].toStringOfTypes())
    hammingDistanceHistogram[mostCommonPath.getDistanceFromOtherPath(uniqueTypes[i])] += uniqueTypesCount[i]


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
    print str(mostCommonSuperPath.getSuperDistanceFromOtherPath(uniqueSuperTypes[i])) + "\t" + str(uniqueSuperTypesCount[i]) + "\t" + str(uniqueSuperTypes[i].toStringOfSuperTypesNoEdges())
    hammingDistanceSuperHistogram[mostCommonSuperPath.getSuperDistanceFromOtherPath(uniqueSuperTypes[i])] += uniqueSuperTypesCount[i]


print "Hamming Distance\tFrequency"

for i in range (0, len(hammingDistanceSuperHistogram)):
    print str(i) + "\t" + str(hammingDistanceSuperHistogram[i])


print '\n' + str(numValid) + " total " + str(maxNumHops) + "-hop synaptic paths from node #" + str(sourceNodeId)

print '\n' + str(len(uniqueTypesCount)) + " unique path types"

print '\n' + str(len(uniqueSuperTypesCount)) + " unique path super types"

print '\n' + str(numNonSynaptic) + " non-synaptic paths were ignored, " + str(numInNetwork) + \
      " in-network paths were ignored; " + str(numNonSynapticAndInNetwork) + " were both."

print '\n' + str(sourceNodeId) + '\t' + str(numValid) + '\t' + str(len(uniqueTypesCount)) + '\t' + \
      str(len(uniqueSuperTypesCount)) + '\t' + str(numNonSynaptic) + '\t' + str(numInNetwork) + '\t' + str(numNonSynapticAndInNetwork)

superTypeFile = open("data/superTypes.csv", "w")
superTypeFile.write("SuperIndex,Path")
nodeTypeFile = open("data/nodeTypes.csv", "w")
nodeTypeFile.write("SuperIndex,NodeIndex,Path")
nodeEdgeTypeFile = open("data/nodeAndEdgeTypes.csv", "w")
nodeEdgeTypeFile.write("SuperIndex,NodeIndex,Path")

#Map super node types -> node types -> node edge types
