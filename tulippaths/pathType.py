__author__ = 'Dasha'

""" Object representing a path type (super type, node type, or node and edge type) """

class PathTypeVertex:
    def __init__(self, dataType, superIndex, nodeIndex, path, frequency):
        self.dataType = dataType
        self.superIndex = superIndex
        self.nodeIndex = nodeIndex
        self.path = path
        self.frequency = int(frequency)
        if self.dataType == "SuperType":
            self._id = "1"
        elif self.dataType == "NodeType":
            self._id = "2"
        else:
            self._id = "3"
        self._id += str(self.superIndex) + str(self.nodeIndex)

    def addFrequency(self, frequency):
        self.frequency += int(frequency)

    def getDataType(self):
        return self.dataType

    def getSuperIndex(self):
        return self.superIndex

    def getNodeIndex(self):
        return self.nodeIndex

    def getPath(self):
        return self.path

    def getId(self):
        return self._id

    def getFrequency(self):
        return self.frequency

class PathTypeEdge:
    def __init__(self, inV, outV, label):
        self.inV = inV
        self.outV = outV
        self.label = label

    def getInV(self):
        return self.inV

    def getOutV(self):
        return self.outV

    def getLabel(self):
        return self.label

class PathType:
    def __init__(self):
        self.vertices = []
        self.edges = []

    def addVertex(self, vertex):
        vertexDict = {
            'id' : int(vertex.getId()),
            'type' : "vertex",
            'dataType' : vertex.getDataType(),
            'superIndex' : int(vertex.getSuperIndex()),
            'nodeIndex' : int(vertex.getNodeIndex()),
            'path' : vertex.getPath(),
            'frequency' : int(vertex.getFrequency())
        }

        self.vertices.append(vertexDict)

    def addEdge(self, edge):
        edgeDict = {
            'type' : "edge",
            'inV' : int(edge.getInV()),
            'outV' : int(edge.getOutV()),
            'label' : edge.getLabel()
        }
        # inV, outV, label
        self.edges.append(edgeDict)

    def getAsJsonObject(self):
        jsonObject = {}
        jsonObject['vertices'] = self.vertices
        jsonObject['edges'] = self.edges

        return jsonObject
