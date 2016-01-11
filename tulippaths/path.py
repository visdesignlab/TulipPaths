""" Object representing a specific path in a graph - nodes and edges """

import utils as utils
import re

class Path:
    # TODO: Smarter default constructor.
    def __init__(self, graph, other=None):
        if other is None:
            self.nodes = []
            self.edges = []
            self.graph = graph
        else:
            self.nodes = list(other.nodes)
            self.edges = list(other.edges)
            self.graph = graph

            assert self.isSane(), 'Warning - created bad path ' + self.toString()

    def addNode(self, node):
        self.nodes.append(node)

    def addEdge(self, edge):
        self.edges.append(edge)

    def getLastNode(self):
        return self.nodes[len(self.nodes) - 1]

    def hasLoop(self):
        return self.nodes[0] in self.nodes[1:]

    def isInTypeConstraints(self, constrainedEdges, constrainedNodes):

        for i in range(0, len(self.edges)):
            edge = self.edges[i]
            edgeType = utils.getEdgeType(edge, self.graph)
            if constrainedEdges[i] != edgeType:
                return False

        for i in range(0, len(self.nodes)):
            node = self.nodes[i]
            nodeType = utils.getNodeType(node, self.graph)
            if constrainedNodes[i] != nodeType:
                return False

        return True

    def isInRegexTypeConstraints(self, constrainedEdgeRegexes,
                                 constrainedNodeRegexes):

        for i in range(0, len(self.edges)):
            edge = self.edges[i]
            edgeType = utils.getEdgeType(edge, self.graph)
            if not re.search(re.compile(constrainedEdgeRegexes[i]), edgeType):
                return False

        for i in range(0, len(self.nodes)):
            node = self.nodes[i]
            nodeType = utils.getNodeType(node, self.graph)
            if not re.search(re.compile(constrainedNodeRegexes[i]), nodeType):
                return False

        return True

    # Returns true if nodes and edges are correctly connected in self.graph.
    def isSane(self):
        sane = True
        for i in range(0, len(self.edges)):
            sane = sane and (self.graph.source(self.edges[i]) == self.nodes[i])
            sane = sane and (self.graph.target(self.edges[i]) == self.nodes[i + 1])
        return sane

    def isSameType(self, other):
        if (not len(self.nodes) == len(other.nodes)) or (not len(self.edges) == len(other.edges)):
            return False

        for i in range(0, len(self.edges)):
            if not utils.getEdgeType(self.edges[i], self.graph) == utils.getEdgeType(other.edges[i], self.graph):
                return False

        for i in range(0, len(self.nodes)):
            if not utils.getNodeType(self.nodes[i], self.graph) == utils.getNodeType(other.nodes[i], self.graph):
                return False

        return True

    # Returns false only if the path contains an edge of type 'adherens' or 'touch'.
    def isSynapticPath(self):
        for edge in self.edges:
            edgeType = utils.getEdgeType(edge, self.graph)
            if edgeType in ['Adherens', 'Touch']:
                return False
        return True

    def size(self):
        return len(self.nodes)

    def toString(self):
        string = ''
        for i in range(0, len(self.edges)):
            string += str(self.nodes[i]) + ', ' + str(self.edges[i]) + ', '
        string += str(self.nodes[len(self.nodes) - 1])
        return string

    def toStringOfIds(self):
        string = ''
        for i in range(0, len(self.edges)):
            string += utils.getNodeId(self.nodes[i], self.graph) + ', '
            string += '(' + utils.getEdgeLinkedStructures(self.edges[i], self.graph) + '), '
        string += utils.getNodeId(self.nodes[len(self.nodes) - 1], self.graph)
        return string

    def toStringOfTypes(self):
        string = ''
        for i in range(0, len(self.edges)):
            string += utils.getNodeType(self.nodes[i], self.graph) + ', '
            string += utils.getEdgeType(self.edges[i], self.graph) + ', '
        string += utils.getNodeType(self.nodes[len(self.nodes) - 1], self.graph)
        return string
