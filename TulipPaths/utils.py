""" Misc utilities for accessing and manipulating tulip graphs """

# Returns an iterator of node with id or raises exception if no node exists.
def getNodeByID(id, nodeIds, graph):
    for node in graph.getNodes():
        if int(nodeIds[node]) == id:
            return node
    assert False, "Failed to find node by id"