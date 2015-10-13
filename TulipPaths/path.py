""" Object representing a specific path in a graph - nodes and edges """


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

    # Returns true if nodes and edges are correctly connected in self.graph.
    def isSane(self):
        sane = True
        for i in range(0, len(self.edges)):
            sane = sane and (self.graph.source(self.edges[i]) == self.nodes[i])
            sane = sane and (self.graph.target(self.edges[i]) == self.nodes[i + 1])
        return sane

    def size(self):
        return len(self.nodes)

    def toString(self):
        string = ''
        for i in range(0, len(self.edges)):
            string = string + str(self.nodes[i]) + ', ' + str(self.edges[i]) + ', '
        string = string + str(self.nodes[len(self.nodes) - 1])
        return string