import utils
from path import *
from pathFinder import *
import copy


class ConnectivityMatrix:
    def __init__(self, graph):
        self._graph = graph
        self._paths = []

        self._nodes = []
        self._initialMatrix = []

        self._matrix = []

        self._rowLabels = []
        self._colLabels = []

        self._sourcesCollapsed = False
        self._targetsCollapsed = False

    def _activateMatrix(self, nodes):

        self._nodes = list(set(nodes))
        for i in range(0, len(self._nodes)):
            row = []
            for j in range(0, len(self._nodes)):
                row.append([])
            self._matrix.append(row)

        for node in self._nodes:
            self._rowLabels.append(utils.getNodeId(node, self._graph))
            self._colLabels.append(utils.getNodeId(node, self._graph))

    def _addPathToMatrix(self, path):
        source = path.nodes[0]
        target = path.nodes[len(path.nodes) - 1]
        assert source in self._nodes and target in self._nodes, 'Found a path that is not in matrix. WTF?'
        self._paths.append(path)
        sourceIndex = self._getNodeIndex(source)
        targetIndex = self._getNodeIndex(target)
        self._matrix[sourceIndex][targetIndex].append(len(self._paths) - 1)

    def _getNodeIndex(self, node):
        return self._nodes.index(node)

    def _getPathAsIndexes(self, path):
        pathIndexes = []
        for i in range(0, len(path.nodes)):
            pathIndexes.append(int(path.nodes[i].id))
            if i < len(path.edges):
                pathIndexes.append(int(path.edges[i].id))
        return pathIndexes

    def _getUsedColIndexes(self):
        usedColIndexes = []
        for i in range(0, len(self._matrix)):
            row = self._matrix[i]
            for j in range(0, len(row)):
                col = row[j]
                if len(col) is not 0 and j not in usedColIndexes:
                    usedColIndexes.append(j)
        return usedColIndexes

    def _getUsedRowIndexes(self):
        usedRowIndexes = []
        for i in range(0, len(self._matrix)):
            row = self._matrix[i]
            for j in range(0, len(row)):
                col = row[j]
                if len(col) is not 0 and i not in usedRowIndexes:
                    usedRowIndexes.append(i)
        return usedRowIndexes

    def activate(self, nodeConstraints, edgeConstraints):
        """
            Create a connectivity matrix for the given path node and edge constraints.

            _matrix[i][j] holds indexes to paths from _nodes[j] to _nodes[i]
            The paths for these indexes can be found in _paths

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
            pathFinder.findRegexConstrainedPaths(node, nodeConstraints, edgeConstraints)
            for path in pathFinder.valid:
                self._addPathToMatrix(path)

        # Cache the initial matrix.
        self._initialMatrix = copy.deepcopy(self._matrix)

    def collapseSources(self):
        """
            Updates _matrix s.t. all rows of the same label get collapsed to a single row.
        """
        if self._sourcesCollapsed:
            return

        sourceTypes = utils.getNodesTypes(self._nodes, self._graph)
        newMatrix = []
        newCols = []
        for node in self._nodes:
            newCols.append(utils.getNodeId(node, self._graph))

        for sourceType in sourceTypes:
            newRow = [[] for node in self._nodes]
            for i in range(0, len(self._matrix)):
                rowType = utils.getNodeType(self._nodes[i], self._graph)
                row = self._matrix[i]
                if rowType == sourceType:
                    for j in range(0, len(row)):
                        col = row[j]
                        if len(col) > 0:
                            newRow[j] += col
            newMatrix.append(newRow)

        self._matrix = copy.deepcopy(newMatrix)
        self._colLabels = newCols
        self._rowLabels = sourceTypes

    def collapseTargets(self):
        """
            Updates _matrix s.t. all cols of the same label get collapsed to a single col.
        """

        if self._targetsCollapsed:
            return

        self._targetsCollapsed = True

        targetTypes = utils.getNodesTypes(self._nodes, self._graph)
        newMatrix = []

        # Initialize newMatrix
        for i in range(0, len(self._matrix)):
            newRow = []
            for j in range(0, len(targetTypes)):
                newRow.append([])
            newMatrix.append(newRow)

        # Populate new matrix
        for i in range(0, len(self._matrix)):
            row = self._matrix[i]
            for j in range(0, len(row)):
                col = row[j]
                if len(col) > 0:
                    colType = utils.getNodeType(self._nodes[j], self._graph)
                    colIndex = targetTypes.index(colType)
                    newMatrix[i][colIndex] += col

        self._matrix = copy.deepcopy(newMatrix)
        self._colLabels = targetTypes

    def getAsJsonObject(self, removeEmptyGridCells=False, replaceCellIdsWithIndexes=False):
        newMatrix = []
        rowLabels = []
        colLabels = []
        if replaceCellIdsWithIndexes and (self._targetsCollapsed or self._sourcesCollapsed):
            assert False, "Cannot replace ids with indexes if sources or targets are collapsed"

        if removeEmptyGridCells:
            usedRows = self._getUsedRowIndexes()
            usedCols = self._getUsedColIndexes()
            newMatrix = []
            for i in range(0, len(usedRows)):
                row = []
                for j in range(0, len(usedCols)):
                    row.append([])
                newMatrix.append(row)

            for i in range(0, len(self._matrix)):
                if i in usedRows:
                    newRowIndex = usedRows.index(i)
                    row = self._matrix[i]
                    for j in range(0, len(row)):
                        if j in usedCols:
                            newColIndex = usedCols.index(j)
                            col = row[j]
                            pathList = []
                            for k in range(0, len(col)):
                                pathList.append(self._getPathAsIndexes(self._paths[col[k]]))

                            newMatrix[newRowIndex][newColIndex] = pathList

            for rowIndex in usedRows:
                rowLabels.append(self._rowLabels[rowIndex])

            for colIndex in usedCols:
                colLabels.append(self._colLabels[colIndex])

        else:
            for row in self._matrix:
                newRow = []
                for col in row:
                    pathList = []
                    for k in range(0, len(col)):
                        pathList.append(self._getPathAsIndexes(self._paths[col[k]]))
                    newRow.append(pathList)
                newMatrix.append(newRow)

            rowLabels = self._rowLabels
            colLabels = self._colLabels

        if replaceCellIdsWithIndexes:
            newRowLabels = []
            for label in rowLabels:
                newRowLabels.append(int(utils.getNodeById(int(label), self._graph).id))
            rowLabels = newRowLabels

            newColLabels = []
            for label in colLabels:
                newColLabels.append(int(utils.getNodeById(int(label), self._graph).id))
            colLabels = newColLabels

        jsonObject = {}
        jsonObject['row_labels'] = rowLabels
        jsonObject['col_labels'] = colLabels
        jsonObject['matrix'] = newMatrix

        return jsonObject

    def getPathAt(self, index):
        return self._paths[index]

    def reset(self):
        self._matrix = copy.deepcopy(self._initialMatrix)

        self._rowLabels = []
        self._colLabels = []
        for node in self._nodes:
            self._rowLabels.append(utils.getNodeId(node, self._graph))
            self._colLabels.append(utils.getNodeId(node, self._graph))

        self._targetsCollapsed = False
        self._sourcesCollapsed = False
