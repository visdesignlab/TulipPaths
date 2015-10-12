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

def getNodeId(node, graph):
    nodeIds = graph.getProperty("ID")
    return nodeIds[node]

def getNodeType(node, graph):
    viewLabels = graph.getProperty("viewLabel")
    return viewLabels[node].split('\n')[0].strip()