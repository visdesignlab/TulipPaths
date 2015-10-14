""" Misc utilities for accessing and manipulating tulip graphs """


def getEdgeType(edge, graph):
    edgeTypes = graph.getProperty("edgeType")
    return edgeTypes[edge]

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

def getNodeId(node, graph):
    nodeIds = graph.getProperty("ID")
    return nodeIds[node]

def getNodeType(node, graph):
    viewLabels = graph.getProperty("viewLabel")
    return viewLabels[node].split('\n')[0].strip()

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