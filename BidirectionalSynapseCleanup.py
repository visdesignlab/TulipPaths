from tulip import *
import tulipplugins
import tulippaths as tp
from FileOutputPlugin import FileOutputPlugin


class BidirectionalSynapseCleanup(FileOutputPlugin):
    def __init__(self, context):
        FileOutputPlugin.__init__(self, context)
        self._edgeTypeLabel = "Edge type"

        self.addStringParameter(self._edgeTypeLabel, "Find edges of this type that are missing a directed link.",
                                "Gap Junction")

    def check(self):
        return (True, "")

    def findInverseEdge(self, graph, source, target, links):
        linkedStructures = graph.getStringProperty("LinkedStructures")
        for edge in graph.getInOutEdges(target):
            if tp.utils.getEdgeType(edge, graph) == self.dataSet[self._edgeTypeLabel]:
                edgeSource = graph.source(edge)
                edgeTarget = graph.target(edge)
                edgeLinks = linkedStructures[edge]
                if edgeSource == target and edgeTarget == source and links == edgeLinks:
                    return True
        return False

    def run(self):
        graph = self.graph

        viewSelection = self.graph.getBooleanProperty("viewSelection")
        linkedStructures = graph.getStringProperty("LinkedStructures")

        self.beginFileOutput()

        # Loop over all edges. If edge is a gap junction, then search for a gap junction going the other direction.
        for edge in graph.getEdges():
            edgeType = tp.utils.getEdgeType(edge, graph)
            if edgeType == self.dataSet[self._edgeTypeLabel]:
                source = graph.source(edge)
                target = graph.target(edge)
                links = linkedStructures[edge]

                if not self.findInverseEdge(graph, source, target, links):
                    output = str(tp.utils.getNodeId(source, graph)) + "-" + tp.utils.getNodeType(source,
                                                                                                 graph) + "; " + str(
                            tp.utils.getNodeId(target, graph)) + "-" + tp.utils.getNodeType(target,
                                                                                            graph) + "; " + links
                    viewSelection[edge] = True

                    self.printToFile(output)

        self.endFileOutput()

        return True


# and updates the GUI to make it accessible through the menus.
tulipplugins.registerPlugin("BidirectionalSynapseCleanup", "Find Missing Bidirectional Synapses", "Kerzner",
                            "12/01/2017", "", "1.0")
