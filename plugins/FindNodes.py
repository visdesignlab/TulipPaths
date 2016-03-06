from tulip import *
import tulipplugins
import tulippaths as tp
import fileOutput
import os.path

class FindNodes(tlp.Algorithm):
    def __init__(self, context):
        tlp.Algorithm.__init__(self, context)

        # Accept one argument: a regex defining possible desired node labels
        self.nodeRegexLabel = "Node Type Regex"
        self.addStringParameter(self.nodeRegexLabel, "", "CBb3m")

        self.outputFileLabel = 'file::Output File'

        # Create an empty output file if none exists
        outputFilename = fileOutput.defaultOutputFile('NodeStats')
        if not os.path.isfile(outputFilename):
            outputFile = open(outputFilename, 'w')
            outputFile.close()

        self.addStringParameter(self.outputFileLabel, "",
                                outputFilename)

    def check(self):
        print("====== Checking input")

        # Retrieve all nodes with labels matching the label regex provided
        nodeRegex = self.dataSet[self.nodeRegexLabel]
        nodes = tp.utils.getNodesByTypeRegex(nodeRegex, self.graph)

        # Report negative if no nodes were found
        if len(nodes) == 0:
            message = 'Could not find nodes matching label regex: ' + nodeRegex

            print(message)
            return (False, message)

        # Report positive if one or more nodes was found
        else:
            message = 'Number of nodes matching label regex ' + nodeRegex + ': ' + str(len(nodes))
            print(message)
            print('\n====== Input passed!\n')
            return (True, "")

    def run(self):
        nodeRegex = self.dataSet[self.nodeRegexLabel]
        viewSelection = self.graph.getBooleanProperty('viewSelection')

        # Deselect every currently selected node
        for node in self.graph.getNodes():
            viewSelection[node] = False

        # Deselect every currently selected edge
        for edge in self.graph.getEdges():
            viewSelection[edge] = False

        # Open the file for saving output
        outputFile = open(self.dataSet[self.outputFileLabel], 'w')

        print("====== Searching for nodes\n")
        print("Type of node (regex): " + nodeRegex)

        # Retrieve all the nodes that match the regex
        nodes = tp.utils.getNodesByTypeRegex(nodeRegex, self.graph)

        print('Total number of nodes found: ' + str(len(nodes)))
        print('\n====== Done searching for nodes\n')

        print("===== Printing node ids\n")

        print(nodeRegex)
        outputFile.write(nodeRegex + '\n')
        for node in nodes:
            print(node.id)
            outputFile.write(str(node.id) + '\n')

        print('\n===== Done printing node ids\n')

        print('===== Printing node statistics')
        outputFile.write('\nStatistics\n')

        # Count the frequency of different specific node types which match
        # the regex
        nodeTypeFrequencies = {}

        for node in nodes:
            nodeType = tp.utils.getNodeType(node, self.graph)
            if nodeType not in nodeTypeFrequencies.keys():
                nodeTypeFrequencies[nodeType] = 1
            else:
                nodeTypeFrequencies[nodeType] += 1

            # Select this node in the graph view
            viewSelection[node] = True

        for nodeType in nodeTypeFrequencies.keys():
            message = 'Percent of matching nodes with type ' + nodeType + ': ' + "{0:.3f}".format(
                    float(nodeTypeFrequencies[nodeType]) / float(len(nodes)))

            print message
            outputFile.write(message + '\n')

        print('\n===== Done printing node statistics\n')

        outputFile.close()
        return True


# The line below does the magic to register the plugin to the plugin database
# and updates the GUI to make it accessible through the menus.
tulipplugins.registerPlugin("FindNodes", "Find Nodes (Regex)", "Nathaniel Nelson", "14/12/2015", "", "1.0")
