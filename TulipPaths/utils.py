# Returns an iterator of node with id or -1 if no node exists
def getNodeByID(id, nodeIds, graph):
    for node in graph.getNodes():
        if int(nodeIds[node]) == id:
            return node
    assert False, "Failed to find node by id"