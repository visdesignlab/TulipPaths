""" Misc utilities for accessing and manipulating tulip graphs """

import tulippaths as tp

# Returns true if node can be reached from sourceTypes.
# sourceTypes is a list of node types (strings).
def canBeReachedFromTypes(node, sourceTypes, graph):
    paths = []
    for edge in graph.getInEdges(node):
        sourceNode = graph.source(edge)
        edgeSourceType = getNodeType(sourceNode, graph)
        edgeType = getEdgeType(edge, graph)
        if edgeSourceType in sourceTypes and edgeType not in ['Adherens', 'Touch']:
            path = tp.Path(graph)
            path.addNode(sourceNode)
            path.addEdge(edge)
            path.addNode(node)

            paths.append(path)

    return paths

# Returns true only if node can reach target types.
# targetTypes is a list of node types (strings).
def canReachTypes(node, targetTypes, graph):
    paths = []
    for edge in graph.getOutEdges(node):
        targetNode = graph.target(edge)
        edgeTargetType = getNodeType(targetNode, graph)
        edgeType = getEdgeType(edge, graph)
        if edgeTargetType in targetTypes and edgeType not in ['Adherens', 'Touch']:
            path = tp.Path(graph)
            path.addNode(node)
            path.addEdge(edge)
            path.addNode(targetNode)
            paths.append(path)
    return paths

def getAllEdgeTypes(graph):
    edgeTypes = []
    for edge in graph.getEdges():
        edgeType = getEdgeType(edge, graph)
        if edgeType not in edgeTypes:
            edgeTypes.append(edgeType)
    return edgeTypes

# Returns a dictionary of nodes: percent completeness
# Max completeness = max number of synapses going into and out of a node
def getApproximateAnnotationCompleteness(graph):
    completeness = {}
    touched = {}

    for node in graph.getNodes():
        touched[node] = 0

    # While there are nodes that we haven't computed completeness values for...
    while 0 in touched.values():

        # Find first available node that we haven't touched.
        for node in graph.getNodes():
            if not touched[node] == 1:
                # Get all nodes of the same type.
                label = getNodeType(node, graph)
                nodes = getNodesByType(label, graph)

                # Count num annotations for all nodes of same type
                numAnnotations = {}
                for localNode in nodes:
                    numAnnotations[localNode] = getApproximateNumAnnotations(localNode, graph)
                    touched[localNode] = 1

                # Find max num of annotations for this type
                maxNumAnnotations = max(numAnnotations.values())

                # Compute completeness as a percent of annotations relative to the most annotated node
                for localNode in nodes:
                    completeness[localNode] = float(numAnnotations[localNode]) / float(maxNumAnnotations)
                    assert completeness[localNode] <= 1.0, 'Error - node has more than 100% completeness'

    return completeness

# Returns an approximate number of annotations for a given cell
def getApproximateNumAnnotations(node, graph):
    approximateNumAnnotations = 0

    for edge in graph.getInOutEdges(node):
        approximateNumAnnotations += getEdgeWeight(edge, graph)

    return approximateNumAnnotations

def getDictionaryOfEdgeTypes(graph):

    dictionary = {}

    for edge in graph.getEdges():

        edgeType = getEdgeType(edge, graph)

        if dictionary.has_key(edgeType):
            dictionary[edgeType].append(edge)
        else:
            dictionary[edgeType] = [edge]

    return dictionary

def getDictionaryOfNodeTypes(graph):

    dictionary = {}

    for node in graph.getNodes():
        nodeType = getNodeType(node, graph)
        if dictionary.has_key(nodeType):
            dictionary[nodeType].append(node)
        else:
            dictionary[nodeType] = [node]

    return dictionary

def getEdgeType(edge, graph):
    edgeTypes = graph.getProperty("edgeType")
    return edgeTypes[edge]

# Returns number of linked children structures that an edge represents.
# AkA number of synapses between 2 nodes
def getEdgeWeight(edge, graph):
    linkedStructures = graph.getProperty("LinkedStructures")
    structures = linkedStructures[edge].strip()
    return len(structures.split('    '))

def getEdgeLinkedStructures(edge, graph):
    linkedStructures = graph.getProperty("LinkedStructures")
    structures = linkedStructures[edge].strip()
    return structures.lstrip(' ')

def getNodeById(id, graph):
    nodeIds = graph.getProperty("ID")
    for node in graph.getNodes():
        if int(nodeIds[node]) == id:
            return node
    assert False, "Failed to find node by id"

def getNodesByType(type, graph):
    nodes = []
    for node in graph.getNodes():
        if getNodeType(node, graph) == type:
            nodes.append(node)
    return nodes

def getNodesByTypes(types, graph):
    nodes = []
    for nodeType in types:
        nodes += getNodesByType(nodeType, graph)
    return nodes

def getNodeId(node, graph):
    nodeIds = graph.getProperty("ID")
    return nodeIds[node]

def getNodeType(node, graph):
    viewLabels = graph.getProperty("viewLabel")
    viewLabel = viewLabels[node].split('\n')
    if len(viewLabel) == 2:
        return viewLabel[0].strip()
    else:
        return 'null'

def isEdgeTypeInGraph(edgeType, graph):
    for edge in graph.getEdges():
        otherType = getEdgeType(edge, graph)
        if otherType == edgeType:
            return True

    return False

def setNodeColor(color, graph):
    viewColor = graph.getColorProperty("viewColor")
    for node in graph.getNodes():
        viewColor[node] = color

def setEdgeColor(color, graph):
    viewColor = graph.getColorProperty("viewColor")
    for edge in graph.getEdges():
        viewColor[edge] = color

def setColor(item, color, graph):
    viewColor = graph.getColorProperty("viewColor")
    viewColor[item] = color

def setPathColor(path, color, graph):
    for node in path.nodes:
        setColor(node, color, graph)
    for edge in path.edges:
        setColor(edge, color, graph)