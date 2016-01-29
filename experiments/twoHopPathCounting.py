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
graphFile = '../data/514_2hops.tlp'
#sourceNodeId = 593
sourceNodeId = 5279
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

print 'The valid paths are:'
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

# check = 0
# for j in range(0, len(uniqueTypesCount)):
#     check = check + uniqueTypesCount[j]
# assert check==len(pathFinder.valid)

# print "Printing unique types counts:"
# for count in uniqueTypesCount:
#    print str(count)

# print "Printing unique super types counts:"
# for count in uniqueSuperTypesCount:
#    print str(count)

print "Types"
for i in range (0, len(uniqueTypesCount)):
    print str(uniqueTypesCount[i]) + "\t" + str(uniqueTypes[i].toStringOfTypes())

print "Super Types"
for i in range (0, len(uniqueSuperTypesCount)):
    print str(uniqueSuperTypesCount[i]) + "\t" + str(uniqueSuperTypes[i].toStringOfSuperTypes())

print '\n' + str(numValid) + " total " + str(maxNumHops) + "-hop synaptic paths from node #" + str(sourceNodeId)

print '\n' + str(len(uniqueTypesCount)) + " unique path types"

print '\n' + str(len(uniqueSuperTypesCount)) + " unique path super types"

print '\n' + str(numNonSynaptic) + " non-synaptic paths were ignored, " + str(numInNetwork) + \
      " in-network paths were ignored; " + str(numNonSynapticAndInNetwork) + " were both."

print '\n' + str(sourceNodeId) + '\t' + str(numValid) + '\t' + str(len(uniqueTypesCount)) + '\t' + \
      str(len(uniqueSuperTypesCount)) + '\t' + str(numNonSynaptic) + '\t' + str(numInNetwork) + '\t' + str(numNonSynapticAndInNetwork)