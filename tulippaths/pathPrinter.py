__author__ = 'Dasha'

import tulippaths as tp
import json

class PathPrinter:
    def __init__(self, graph):
         self.graph = graph

    def printToFile(self, sourceNodeId, jsonFile):

        maxNumHops = 2

        # Find start node
        source = tp.getNodeById(sourceNodeId, self.graph)

        # Find paths
        pathFinder = tp.PathFinder(self.graph)
        results = pathFinder.findAllPaths(source, maxNumHops)

        pathJsonObject = tp.PathType(sourceNodeId)

        superTypeDict = {}
        superTypes = []
        nodeTypes = []
        nodeAndEdgeTypes = []

        numNonSynaptic = 0
        numValid = 0
        numInNetwork = 0
        numNonSynapticAndInNetwork = 0

        superTypeIndex = 0

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

            numValid += 1

            superTypeString = path.toStringOfNodeSuperTypes()
            # Case 1: Super type has not been seen before, so we need to add new Super Type, Node Type, and Node and Edge Type
            if superTypeString not in superTypeDict:
                superVertex = tp.PathTypeVertex("SuperType", superTypeIndex, 0, 0, superTypeString, 1)
                # To make searching for super types quick
                superTypeDict[superTypeString] = superVertex
                # Using array/list here to make getting super types out sequentially later easy
                superTypes.append(superVertex)
                nodeTypes.append([tp.PathTypeVertex("NodeType", superTypeIndex, 0, 0, path.toStringOfNodeTypes(), 1)])
                nodeAndEdgeTypes.append([[tp.PathTypeVertex("NodeAndEdgeType", superTypeIndex, 0, 0, path.toStringOfTypesJson(), 1)]])
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
                    nodeTypes[currentSuperTypeIndex].append(tp.PathTypeVertex("NodeType", currentSuperTypeIndex, nodeIndex, 0, nodeTypeString, 1))
                    nodeAndEdgeTypes[currentSuperTypeIndex].append([tp.PathTypeVertex("NodeAndEdgeType", currentSuperTypeIndex, nodeIndex, 0, nodeAndEdgeTypeString, 1)])
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
                        nodeAndEdgeTypes[currentSuperTypeIndex][nodeIndex].append(tp.PathTypeVertex("NodeAndEdgeType", currentSuperTypeIndex, nodeIndex, len(nodeAndEdgeTypes[currentSuperTypeIndex][nodeIndex]), nodeAndEdgeTypeString, 1))

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

        jsonFile = open(jsonFile, "w")
        jsonObject = pathJsonObject.getAsJsonObject()
        jsonFile.write(json.dumps(jsonObject, sort_keys=True, indent=4, separators=(',', ': ')))