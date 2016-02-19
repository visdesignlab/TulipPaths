import tulippaths as tp

def getEdgeAttributes():
    edgeAttributes = []
    edgeAttributes.append({
        "Name": "ID",
        "DisplayName": "id",
        "Type": "int",
        "DataType": "index",
        "Unique": "true"
    })

    edgeAttributes.append({
        "Name": "SourceID",
        "DisplayName": "source id",
        "Type": "int",
        "DataType": "source-index",
        "Unique": "false"
    })

    edgeAttributes.append({
        "Name": "TargetID",
        "DisplayName": "target id",
        "Type": "int",
        "DataType": "target-index",
        "Unique": "true"
    })

    edgeAttributes.append({
        "Name": "TargetID",
        "DisplayName": "target id",
        "Type": "int",
        "DataType": "target-index",
        "Unique": "true"
    })

    edgeAttributes.append({
        "Name": "Type",
        "DisplayName": "edge type",
        "Type": "string",
        "DataType": "categorical",
        "Unique": "false"
    })

    edgeAttributes.append({
        "Name": "LinkedStructures",
        "DisplayName": "structures",
        "Type": "string",
        "DataType": "string",
        "Unique": "false"
    })

    return edgeAttributes


def getNodeAttributes():
    nodeAttributes = []

    nodeAttributes.append({
        "Name": "ID",
        "DisplayName": "id",
        "Type": "int",
        "DataType": "index",
        "Unique": "true"
    })

    nodeAttributes.append({
        "Name": "Label",
        "DisplayName": "label",
        "Type": "string",
        "DataType": "categorical",
        "Unique": "false"
    })

    nodeAttributes.append({
        "Name": "StructureID",
        "DisplayName": "structure",
        "Type": "int",
        "DataType": "id",
        "Unique": "true"
    })

    nodeAttributes.append({
        "Name": "Completeness",
        "DisplayName": "completeness",
        "Type": "float",
        "DataType": "quantitative",
        "Unique": "false"
    })

    nodeAttributes.append({
        "Name": "HullArea",
        "DisplayName": "area",
        "Type": "float",
        "DataType": "quantitative",
        "Unique": "false"
    })

    nodeAttributes.append({
        "Name": "Locations",
        "DisplayName": "locations",
        "Type": "int",
        "DataType": "quantitative",
        "Unique": "false"
    })

    return nodeAttributes


def graphToJson(graph):
    completeness = tp.utils.getApproximateAnnotationCompleteness(graph)
    nodes = []
    edges = []
    hullArea = graph.getDoubleProperty("hull area")
    locations = graph.getDoubleProperty("locations")
    for node in graph.getNodes():
        dictionary = {
            "ID": int(node.id),
            "Label": tp.utils.getNodeType(node, graph),
            "StructureID": int(tp.utils.getNodeId(node, graph)),
            "Completeness": completeness[node],
            "HullArea": hullArea[node],
            "Locations": locations[node]
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

    nodeAttributes = getNodeAttributes()
    edgeAttributes = getEdgeAttributes()

    return {
        "nodeAttributes": nodeAttributes,
        "nodes": nodes,
        "edgeAttributes": edgeAttributes,
        "edges": edges
    }
