from tulip import *
import tulipplugins
import tulippaths as tp


class FindPaths(tlp.Algorithm):
    def __init__(self, context):
        tlp.Algorithm.__init__(self, context)

        self.nodeLabel0 = "node #0 label"
        self.nodeLabel1 = "node #1 label"
        self.nodeLabel2 = "node #2 label"

        self.edgeType0 = "edge #0 type"
        self.edgeType1 = "edge #1 type"

        self.outputFileLabel = 'Output file'

        # These default values will find one path in the file data\test_feedback.tlp!
        self.addStringParameter(self.nodeLabel0, "", "CBb3m")
        self.addStringParameter(self.edgeType0, "", "Ribbon Synapse")
        self.addStringParameter(self.nodeLabel1, "", "IAC")
        self.addStringParameter(self.edgeType1, "", "Conventional")
        self.addStringParameter(self.nodeLabel2, "", "GC")
        self.addStringParameter(self.outputFileLabel, "", "C:\Users\kerzner\PathStats.txt")

    def check(self):
        print "====== Checking inputs"

        print    "\n== Checking node types"
        nodeTypes = self.getNodeTypeConstraints()
        for nodeType in nodeTypes:
            nodes = tp.utils.getNodesByType(nodeType, self.graph)
            if len(nodes) == 0:
                print "\n====== Could not find nodes of type: " + nodeType + "\n"
                return (False, "Could not find nodes of type: " + nodeType)
            else:
                print "Num nodes with type " + nodeType + ": " + str(len(nodes))

        print    "\n== Checking edge types"
        edgeTypes = self.getEdgeTypeConstraints()
        allEdgesByType = tp.utils.getDictionaryOfEdgeTypes(self.graph)
        for edgeType in edgeTypes:
            if edgeType not in allEdgesByType.keys():
                print "\n====== Could not find edges of type: " + edgeType + "!\n"
                return (False, "Could not find edges of type: " + edgeType)
            else:
                print "Num edges with type " + edgeType + ": " + str(len(allEdgesByType[edgeType]))

        print "\n====== Inputs passed!\n"

        return (True, "")

    def getEdgeTypeConstraints(self):
        edgeTypes = []
        edgeTypes.append(self.dataSet[self.edgeType0].strip())
        edgeTypes.append(self.dataSet[self.edgeType1].strip())
        return edgeTypes

    def getNodeTypeConstraints(self):
        nodeTypes = []
        nodeTypes.append(self.dataSet[self.nodeLabel0].strip())
        nodeTypes.append(self.dataSet[self.nodeLabel1].strip())
        nodeTypes.append(self.dataSet[self.nodeLabel2].strip())
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

        outputFile = open(self.dataSet[self.outputFileLabel], 'w')

        pathTypeString = nodeTypes[0] + ", " + edgeTypes[0] + ", " + nodeTypes[1] + ", " + edgeTypes[1] + ", " + \
                         nodeTypes[2]

        print "====== Searching for paths\n"
        print "Type of path: " + pathTypeString

        wrapper = tp.PathFinderWrapper(self.graph)
        paths = wrapper.findConstrainedPathsFromType(sourceType, edgeTypes, nodeTypes)

        print "Total num paths found: " + str(len(paths))
        print "\n====== Done searching for paths\n"

        print "===== Printing path ids\n"

        print pathTypeString
        outputFile.write(pathTypeString + '\n')
        for path in paths:

            if not path.toStringOfTypes() == pathTypeString:
                print "Something went wrong. I found a path type that does not match!"
                print path.toStringOfTypes()
                return False

            print path.toStringOfIds()
            outputFile.write(path.toStringOfIds() + '\n')

        print "\n===== Done printing path ids\n"
        # Print those paths

        print "===== Printing path statistics\n"
        outputFile.write("\nStatistics\n")

        sourceNodesWithPath = []
        targetNodesWithPath = []

        for path in paths:

            if path.nodes[0] not in sourceNodesWithPath:
                sourceNodesWithPath.append(path.nodes[0])

            if path.nodes[2] not in targetNodesWithPath:
                targetNodesWithPath.append(path.nodes[2])

            for node in path.nodes:
                viewSelection[node] = True

            for edge in path.edges:
                viewSelection[edge] = True

        nodeTypeDictionary = tp.utils.getDictionaryOfNodeTypes(self.graph)
        nodesInPath = "Percent of " + nodeTypes[0] + " nodes part of a path: " + "{0:.3f}".format(
                float(len(sourceNodesWithPath)) / float(len(nodeTypeDictionary[nodeTypes[0]])))
        print nodesInPath

        outputFile.write(nodesInPath + '\n')
        nodesInPath = "Percent of " + nodeTypes[2] + " nodes part of a path: " + "{0:.3f}".format(
                float(len(targetNodesWithPath)) / float(len(nodeTypeDictionary[nodeTypes[2]])))

        print nodesInPath
        outputFile.write(nodesInPath + '\n')

        print "\n===== Done printing path statistics\n"

        return True


# The line below does the magic to register the plugin to the plugin database
# and updates the GUI to make it accessible through the menus.
tulipplugins.registerPlugin("FindPaths", "Find 2-Hop Paths", "", "14/12/2015", "", "1.0")
