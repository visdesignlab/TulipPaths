from FileOutputPlugin import FileOutputPlugin
from tulip import *
import tulippaths as tp

exampleCellLabels = ['CBb4w', 'CBb4w', 'AC', 'Rod BC', 'Rod BC']
exampleEdgeTypes = ['.*', '.*', '.*', '.*']


class FindPathsPlugin(FileOutputPlugin):
    """ Tulip plugin algorithm which searches for paths that match a series of
    regexes defining desired labels for nodes and edges in sequence
    """

    def __init__(self, context, hops):
        FileOutputPlugin.__init__(self, context)

        self.hops = hops

        # Accept as a parameter a cell label regex for the initial cell plus
        # one per hop this algorithm is initialized to handle
        self._nodeLabels = []

        for i in range(self.hops + 1):
            self._nodeLabels.append('Node #' + str(i) + ' Label Regex')

        # Accept as a parameter an edge type regex for each hop this algorithm
        # is initialized to handle
        self._edgeTypes = []
        for i in range(self.hops):
            self._edgeTypes.append('Edge #' + str(i) + ' Type Regex')

        # Add all the parameters we need in an intuitive sequence
        for i in range(self.hops):
            self.addStringParameter(self._nodeLabels[i], "", exampleCellLabels[i])
            self.addStringParameter(self._edgeTypes[i], "", exampleEdgeTypes[i])
        self.addStringParameter(self._nodeLabels[self.hops], "", exampleCellLabels[self.hops])

    def check(self):
        nodeTypes = self.getNodeTypeConstraints()
        for nodeType in nodeTypes:
            nodes = tp.utils.getNodesByTypeRegex(nodeType, self.graph)
            if len(nodes) == 0:
                return False, "Could not find nodes matching type regex: " + nodeType

        edgeTypes = self.getEdgeTypeConstraints()

        for edgeType in edgeTypes:
            edges = tp.utils.getEdgesByTypeRegex(edgeType, self.graph)
            if len(edges) == 0:
                return False, "Could not find edges matching type regex: " + edgeType

        return True, ""

    def getEdgeTypeConstraints(self):
        edgeTypes = []
        for i in range(self.hops):
            edgeTypes.append(self.dataSet[self._edgeTypes[i]].strip())
        return edgeTypes

    def getNodeTypeConstraints(self):
        nodeTypes = []
        for i in range(self.hops + 1):
            nodeTypes.append(self.dataSet[self._nodeLabels[i]].strip())
        return nodeTypes

    def run(self):
        nodeTypes = self.getNodeTypeConstraints()
        edgeTypes = self.getEdgeTypeConstraints()

        viewSelection = self.graph.getBooleanProperty("viewSelection")

        for node in self.graph.getNodes():
            viewSelection[node] = False

        for edge in self.graph.getEdges():
            viewSelection[edge] = False

        self.beginFileOutput()

        pathTypeString = ''
        for i in range(self.hops):
            pathTypeString += nodeTypes[i] + ", " + edgeTypes[i] + ", "
        pathTypeString += nodeTypes[self.hops]

        wrapper = tp.PathFinderWrapper(self.graph)
        paths = wrapper.findRegexConstrainedPaths(nodeTypes, edgeTypes)

        # Write the file header
        self.printToFile("Plugin: Find " + str(self.hops) + "-hop paths")
        query = ""
        for i in range(self.hops):
            query += " " + nodeTypes[i] + ","
            query += " " + edgeTypes[i] + ","
        query += " " + nodeTypes[self.hops]
        self.printToFile("Query:" + query)
        self.printToFile("Num paths found: " + str(len(paths)))

        # First check how many different types of paths have matched the regex
        # specifications
        pathTypesFound = set()
        for path in paths:
            pathTypesFound.add(path.toStringOfTypes())

        # Now print every path as a list of IDs, but grouped together by path
        # type
        for pathType in pathTypesFound:
            self.printToFile(pathType)
            for path in paths:
                if pathType == path.toStringOfTypes():
                    self.printToFile(path.toStringOfIds())

        for path in paths:
            # Mark all parts of the path as visually selected
            for node in path.nodes:
                viewSelection[node] = True
            for edge in path.edges:
                viewSelection[edge] = True

        self.endFileOutput()

        return True
