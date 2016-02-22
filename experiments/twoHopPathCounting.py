__author__ = 'Dasha'

from tulip import *
import tulippaths as tp
import json

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

pathJsonObject = tp.PathType()

superTypeDict = {}
superTypes = []
nodeTypes = []
nodeAndEdgeTypes = []

# uniqueNodeAndEdgeTypeDict = {}
# uniqueNodeAndEdgeTypes = []
# uniqueNodeAndEdgeTypesCount = []
# uniqueNodeTypeDict = {}
# uniqueNodeTypes = []
# uniqueNodeTypesCount = []
# uniqueSuperTypes = []
# uniqueSuperTypesCount = []
numNonSynaptic = 0
numValid = 0
numInNetwork = 0
numNonSynapticAndInNetwork = 0

superTypeIndex = 0
nodeTypeIndex = 0

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

    superTypeString = path.toStringOfNodeSuperTypes()
    # Case 1: Super type has not been seen before, so we need to add new Super Type, Node Type, and Node and Edge Type
    if superTypeString not in superTypeDict:
        superVertex = tp.PathTypeVertex("SuperType", superTypeIndex, 0, superTypeString, 1)
        # To make searching for super types quick
        superTypeDict[superTypeString] = superVertex
        # Using array/list here to make getting super types out sequentially later easy
        superTypes.append(superVertex)
        nodeTypes.append([tp.PathTypeVertex("NodeType", superTypeIndex, 0, path.toStringOfNodeTypes(), 1)])
        nodeAndEdgeTypes.append([[tp.PathTypeVertex("NodeAndEdgeType", superTypeIndex, 0, path.toStringOfTypesJson(), 1)]])
        superTypeIndex+=1
    else:
        currentSuperTypeIndex = superTypeDict[superTypeString].getSuperIndex()
        superTypes[currentSuperTypeIndex].addFrequency(1)
        nodeTypeString = path.toStringOfNodeTypes()
        nodeAndEdgeTypeString = path.toStringOfTypesJson()
        nodeIndex = 0
        found = False
        for j in range(0, len(nodeTypes[currentSuperTypeIndex])):
            # Case 2: Super Type is found, and Node Type is found; update Node Type frequency
            if nodeTypes[currentSuperTypeIndex][j].getPath() == nodeTypeString:
                nodeTypes[currentSuperTypeIndex][j].addFrequency(1)
                nodeIndex = j
                found = True
                break
        # Case 3: Super Type is found, but Node Type is new. Add new Node Type and Node and Edge type to the appropriate indices
        if not found:
            nodeIndex = len(nodeTypes[currentSuperTypeIndex])
            nodeTypes[currentSuperTypeIndex].append(tp.PathTypeVertex("NodeType", currentSuperTypeIndex, nodeIndex, nodeTypeString, 1))
            nodeAndEdgeTypes[currentSuperTypeIndex].append([tp.PathTypeVertex("NodeAndEdgeType", currentSuperTypeIndex, nodeIndex, nodeAndEdgeTypeString, 1)])
        else:
            found = False
            for j in range(0, len(nodeAndEdgeTypes[currentSuperTypeIndex][nodeIndex])):
                # Case 2a: Super Type is found, Node Type is found, and Node and Edge type is also found. Update node and edge frequency
                if nodeAndEdgeTypes[currentSuperTypeIndex][nodeIndex][j].getPath() == nodeAndEdgeTypeString:
                    nodeAndEdgeTypes[currentSuperTypeIndex][nodeIndex][j].addFrequency(1)
                    found = True
                    break
            # Case 2b: Super Type is found, Node Type is found, but Node and Edge type is not. Add new Node and Edge type.
            if not found:
                nodeAndEdgeTypes[currentSuperTypeIndex][nodeIndex].append(tp.PathTypeVertex("NodeAndEdgeType", currentSuperTypeIndex, nodeIndex, nodeAndEdgeTypeString, 1))

# Walk through super types, node types, and node and edge types; add vertices and edges, respectively
# Note: inV is the "parent" vertex, and outV is the "child"
for superIndex in range(0, len(superTypes)):
    pathJsonObject.addVertex(superTypes[superIndex])
    outV = superTypes[superIndex].getId()
    inV = 0
    for nodeIndex in range(0, len(nodeTypes[superIndex])):
        inV = nodeTypes[superIndex][nodeIndex].getId()
        pathJsonObject.addVertex(nodeTypes[superIndex][nodeIndex])
        pathJsonObject.addEdge(tp.PathTypeEdge(inV, outV, "superToNodeType"))

        nodeTypeOutV = nodeTypes[superIndex][nodeIndex].getId()
        for nodeAndEdgeIndex in range(0, len(nodeAndEdgeTypes[superIndex][nodeIndex])):
            inV = nodeAndEdgeTypes[superIndex][nodeIndex][nodeAndEdgeIndex].getId()
            pathJsonObject.addVertex(nodeAndEdgeTypes[superIndex][nodeIndex][nodeAndEdgeIndex])
            pathJsonObject.addEdge(tp.PathTypeEdge(inV, nodeTypeOutV, "nodeToNodeAndEdgeType"))

jsonFile = open("../data/jsonFile.json", "w")
jsonObject = pathJsonObject.getAsJsonObject()
jsonFile.write(json.dumps(jsonObject, sort_keys=True, indent=4, separators=(',', ': ')))
# print json.dumps(jsonObject)

### Old code from here on ###

    # found = False
    # for j in range(0, len(uniqueNodeAndEdgeTypes)):
    #     other = uniqueNodeAndEdgeTypes[j]
    #     if path.isSameType(other):
    #         uniqueNodeAndEdgeTypesCount[j] += 1
    #         found = True
    #         break
    #
    # if not found:
    #     uniqueNodeTypes.append(path)
    #     uniqueNodeTypesCount.append(1)
    #
    # found = False
    # for j in range(0, len(uniqueNodeTypes)):
    #     other = uniqueNodeTypes[j]
    #     if path.isSameNodeType(other):
    #         uniqueNodeTypesCount[j] += 1
    #         found = True
    #         break
    #
    # if not found:
    #     uniqueNodeTypes.append(path)
    #     uniqueNodeTypesCount.append(1)
    #
    # # Same thing for super types
    # found = False
    # for j in range(0, len(uniqueSuperTypes)):
    #     other = uniqueSuperTypes[j]
    #     if path.isSameSuperType(other):
    #         uniqueSuperTypesCount[j] += 1
    #         found = True
    #         break
    #
    # if not found:
    #     uniqueSuperTypes.append(path)
    #     uniqueSuperTypesCount.append(1)

# mostCommonPath = uniqueNodeTypes[0]
# pathFrequency = uniqueNodeTypesCount[0]
# hammingDistanceHistogram = [0, 0, 0, 0, 0, 0]

# print "Types"
# for i in range (0, len(uniqueNodeTypesCount)):
#     print str(uniqueNodeTypesCount[i]) + "\t" + str(uniqueNodeTypes[i].toStringOfTypes())
#     if(pathFrequency < uniqueNodeTypesCount[i]):
#         pathFrequency = uniqueNodeTypesCount[i]
#         mostCommonPath = uniqueNodeTypes[i]

# mostCommonSuperPath = uniqueSuperTypes[0]
# superPathFrequency = uniqueSuperTypesCount[0]
# hammingDistanceSuperHistogram = [0, 0, 0, 0, 0, 0]

# for i in range (0, len(uniqueSuperTypesCount)):
#     # print str(uniqueTypesCount[i]) + "\t" + str(uniqueTypes[i].toStringOfTypes())
#     if(superPathFrequency < uniqueSuperTypesCount[i]):
#         superPathFrequency = uniqueSuperTypesCount[i]
#         mostCommonSuperPath = uniqueSuperTypes[i]
#
# print "Super Types"
# for i in range (0, len(uniqueSuperTypesCount)):
#     print str(uniqueSuperTypesCount[i]) + "\t" + str(uniqueSuperTypes[i].toStringOfSuperTypes())
#
# print "\nMost common path is " + str(mostCommonPath.toStringOfTypes())
# print "Distances from other paths:"
#
# print "\nHamming Distance\tFrequency\tPath"
#
# for i in range (0, len(uniqueNodeTypesCount)):
#     toPrint = ""
#     # for j in range (0, len(uniqueTypesCount)):
#         # toPrint += str(uniqueTypes[i].getDistanceFromOtherPath(uniqueTypes[j])) + "\t"
#     # print toPrint
#     print str(mostCommonPath.getDistanceFromOtherPath(uniqueNodeTypes[i])) + "\t" + str(uniqueNodeTypesCount[i]) + "\t" + str(uniqueNodeTypes[i].toStringOfTypes())
#     hammingDistanceHistogram[mostCommonPath.getDistanceFromOtherPath(uniqueNodeTypes[i])] += uniqueNodeTypesCount[i]
#
#
# print "Hamming Distance\tFrequency"
#
# for i in range (0, len(hammingDistanceHistogram)):
#     print str(i) + "\t" + str(hammingDistanceHistogram[i])
#
# print "********************"
# print "Super types"
# print "\nHamming Distance\tFrequency\tPath"
# for i in range (0, len(uniqueSuperTypesCount)):
#     toPrint = ""
#     # for j in range (0, len(uniqueTypesCount)):
#         # toPrint += str(uniqueTypes[i].getDistanceFromOtherPath(uniqueTypes[j])) + "\t"
#     # print toPrint
#     print str(mostCommonSuperPath.getSuperDistanceFromOtherPath(uniqueSuperTypes[i])) + "\t" + str(uniqueSuperTypesCount[i]) + "\t" + str(uniqueSuperTypes[i].toStringOfNodeTypes())
#     hammingDistanceSuperHistogram[mostCommonSuperPath.getSuperDistanceFromOtherPath(uniqueSuperTypes[i])] += uniqueSuperTypesCount[i]
#
#
# print "Hamming Distance\tFrequency"
#
# for i in range (0, len(hammingDistanceSuperHistogram)):
#     print str(i) + "\t" + str(hammingDistanceSuperHistogram[i])
#
#
# print '\n' + str(numValid) + " total " + str(maxNumHops) + "-hop synaptic paths from node #" + str(sourceNodeId)
#
# print '\n' + str(len(uniqueNodeTypesCount)) + " unique path types"
#
# print '\n' + str(len(uniqueSuperTypesCount)) + " unique path super types"
#
# print '\n' + str(numNonSynaptic) + " non-synaptic paths were ignored, " + str(numInNetwork) + \
#       " in-network paths were ignored; " + str(numNonSynapticAndInNetwork) + " were both."
#
# print '\n' + str(sourceNodeId) + '\t' + str(numValid) + '\t' + str(len(uniqueNodeTypesCount)) + '\t' + \
#       str(len(uniqueSuperTypesCount)) + '\t' + str(numNonSynaptic) + '\t' + str(numInNetwork) + '\t' + str(numNonSynapticAndInNetwork)

# superTypeFile.write("SuperIndex,Path,Frequency")
# nodeTypeFile = open("../data/nodeTypes.json", "w")
# nodeTypeFile.write("SuperIndex,NodeIndex,Path,Frequency")
# nodeEdgeTypeFile = open("../data/nodeAndEdgeTypes.json", "w")
# nodeEdgeTypeFile.write("SuperIndex,NodeIndex,Path,Frequency")

#Map super node types -> node types -> node edge types
