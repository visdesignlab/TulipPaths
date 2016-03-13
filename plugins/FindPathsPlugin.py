from FileOutputPlugin import FileOutputPlugin
from tulip import *
import tulippaths as tp


exampleCellLabel = 'CBb3m'
exampleEdgeType = 'Ribbon Synapse'


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

        for i in range(self.hops+1):
            self._nodeLabels.append('Node #' + str(i) + ' Label Regex')

        # Accept as a parameter an edge type regex for each hop this algorithm
        # is initialized to handle
        self._edgeTypes = []
        for i in range(self.hops):
            self._edgeTypes.append('Edge #' + str(i) + ' Type Regex')

        # Add all the parameters we need in an intuitive sequence
        for i in range(self.hops):
            self.addStringParameter(self._nodeLabels[i], "", exampleCellLabel)
            self.addStringParameter(self._edgeTypes[i], "", exampleEdgeType)
        self.addStringParameter(self._nodeLabels[self.hops], "", exampleCellLabel)

    def check(self):
        print "====== Checking inputs"

        print "\n== Checking node types"
        nodeTypes = self.getNodeTypeConstraints()
        for nodeType in nodeTypes:
            nodes = tp.utils.getNodesByTypeRegex(nodeType, self.graph)
            if len(nodes) == 0:
                print "\n====== Could not find nodes matching type regex: " + nodeType + "\n"
                return (False, "Could not find nodes matching type regex: " + nodeType)
            else:
                print "Num nodes matching type regex " + nodeType + ": " + str(len(nodes))

        print    "\n== Checking edge types"
        edgeTypes = self.getEdgeTypeConstraints()
        for edgeType in edgeTypes:
            edges = tp.utils.getEdgesByTypeRegex(edgeType, self.graph)
            if len(edges) == 0:
                print "\n====== Could not find edges matching type regex: " + edgeType + "!\n"
                return (False, "Could not find edges matching type regex: " + edgeType)
            else:
                print "Num edges matching type regex " + edgeType + ": " + str(len(edges))

        print "\n====== Inputs passed!\n"

        return (True, "")

    def getEdgeTypeConstraints(self):
        edgeTypes = []
        for i in range(self.hops):
            edgeTypes.append(self.dataSet[self._edgeTypes[i]].strip())
        return edgeTypes

    def getNodeTypeConstraints(self):
        nodeTypes = []
        for i in range(self.hops+1):
            nodeTypes.append(self.dataSet[self._nodeLabels[i]].strip())
        return nodeTypes

    def run(self):
        nodeTypes = self.getNodeTypeConstraints()
        edgeTypes = self.getEdgeTypeConstraints()
        sourceType = nodeTypes[0]
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

        print "====== Searching for paths\n"
        print "Type of path: " + pathTypeString

        wrapper = tp.PathFinderWrapper(self.graph)
        paths = wrapper.findConstrainedPathsFromTypeRegex(sourceType, nodeTypes, edgeTypes)

        print "Total num paths found: " + str(len(paths))
        print "\n====== Done searching for paths\n"

        print "===== Printing path ids\n"

        # First check how many different types of paths have matched the regex
        # specifications
        pathTypesFound = set()
        for path in paths:
            pathTypesFound.add(path.toStringOfTypes())

        # Now print every path as a list of IDs, but grouped together by path
        # type
        for pathType in pathTypesFound:
            print pathType
            self.printToFile(pathType)
            for path in paths:
                if pathType == path.toStringOfTypes():
                    print path.toStringOfIds()
                    self.printToFile(path.toStringOfIds())

        print "\n===== Done printing path ids\n"

        # print "===== Printing path statistics\n"
        # self.printToFile()
        # self.printToFile('Statistics')

        # sourceNodesWithPath = []
        # targetNodesWithPath = []

        for path in paths:

            # if path.nodes[0] not in sourceNodesWithPath:
                # sourceNodesWithPath.append(path.nodes[0])

            # if path.nodes[2] not in targetNodesWithPath:
                # targetNodesWithPath.append(path.nodes[2])

            # Mark all parts of the path as visually selected
            for node in path.nodes:
                viewSelection[node] = True
            for edge in path.edges:
                viewSelection[edge] = True

        # nodeTypeDictionary = tp.utils.getDictionaryOfNodeTypes(self.graph)
        # nodesInPath =  "Percent of " + nodeTypes[0] + " nodes part of a path: " + "{0:.3f}".format(
            # float(len(sourceNodesWithPath)) / float(len(nodeTypeDictionary[nodeTypes[0]])))

        # print nodesInPath
        # self.printToFile(nodesInPath)

        # nodesInPath = "Percent of " + nodeTypes[self.hops] + " nodes part of a path: " + "{0:.3f}".format(
            # float(len(targetNodesWithPath)) / float(len(nodeTypeDictionary[nodeTypes[self.hops]])))

        # print nodesInPath
        # self.printToFile(nodesInPath)


        # print "\n===== Done printing path statistics\n"

        self.endFileOutput()

        return True
