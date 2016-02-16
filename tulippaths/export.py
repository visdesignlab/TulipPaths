import tulippaths as tp


def graphToJson(graph):
    completeness = tp.utils.getApproximateAnnotationCompleteness(graph)
    nodes = []
    edges = []

    for node in graph.getNodes():
        dictionary = {
            "ID": int(node.id),
            "Label": tp.utils.getNodeType(node, graph),
            "StructureID": int(tp.utils.getNodeId(node, graph)),
            "Completeness": completeness[node]
        }
        nodes.append(dictionary)

    for edge in graph.getEdges():
        source = graph.source(edge)
        target = graph.target(edge)
        dictionary = {
            "ID": edge.id,
            "SourceStructureID": int(tp.utils.getNodeId(source, graph)),
            "TargetStructureID": int(tp.utils.getNodeId(target, graph)),
            "SourceID": int(source.id),
            "TargetID": int(target.id),
            "Type": tp.utils.getEdgeType(edge, graph),
            "LinkedStructures": tp.utils.getEdgeLinkedStructures(edge, graph)
        }
        edges.append(dictionary)

    return {
        "nodes": nodes,
        "edges": edges
    }
