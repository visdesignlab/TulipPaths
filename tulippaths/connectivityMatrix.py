import utils
from path import *
from pathFinder import *

class ConnectivityMatrix:
    def __init__(self, graph):
        self._graph = graph
        self._paths = []
        self._nodes = []
        self._matrix = []

    def _activateMatrix(self, nodes):
        self._nodes = list(set(nodes))
        for i in range(0, len(self._nodes)):
            row = []
            for j in range(0, len(self._nodes)):
                row.append([])
            self._matrix.append(row)

    def _addPathToMatrix(self, path):
        source = path.nodes[0]
        target = path.nodes[len(path.nodes) - 1]
        assert source in self._nodes and target in self._nodes, 'Found a path that is not in matrix. WTF?'
        sourceIndex = self._getNodeIndex(source)
        targetIndex = self._getNodeIndex(target)
        self._matrix[sourceIndex][targetIndex].append(path)

    def _getNodeIndex(self, node):
        return self._nodes.index(node)

    def activate(self, nodeConstraints, edgeConstraints):
        """
            Create a connectivity matrix for the given path node and edge constraints.

            :param nodeConstraints - regex of all nodes
            :param edgeConstraints - regex of all edges
        """

        # Matrix is N x N where N is the number of sources and targets.
        sources = utils.getNodesByTypeRegex(nodeConstraints[0], self._graph)
        targets = utils.getNodesByTypeRegex(nodeConstraints[len(nodeConstraints) - 1], self._graph)
        nodes = sources + targets
        self._activateMatrix(nodes)

        # Find paths for each source. Shove them into the matrix.
        for node in sources:
            pathFinder = PathFinder(self._graph)
            pathFinder.findRegexConstrainedPaths(node, edgeConstraints, nodeConstraints)
            for path in pathFinder.valid:
                self._addPathToMatrix(path)

    def getPathCountJsonMatrix(self):
        newMatrix = []
        rowLabels = []

        for row in self._matrix:
            newRow = []
            for col in row:
                newRow.append(len(col))
            newMatrix.append(newRow)

        for node in self._nodes:
            rowLabels.append(utils.getNodeId(node, self._graph))

        colLabels = rowLabels

        jsonObject = {}
        jsonObject['row_labels'] = rowLabels
        jsonObject['col_labels'] = colLabels
        jsonObject['matrix'] = newMatrix

        return jsonObject