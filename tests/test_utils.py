from unittest import TestCase

from tulip import *
import TulipPaths as tp

class TestUtils(TestCase):

    def setUp(self):
        self.file = '../data/test_zero.tlp'
        self.graph = tlp.loadGraph(self.file)


    def test_getEdgeType(self):
        edgeType = 0

        for edge in self.graph.getEdges():
            edgeType = tp.utils.getEdgeType(edge, self.graph)

        self.assertTrue(edgeType == 'Ribbon Synapse')

    def test_getNodeById(self):
        nodeId = 606
        node = tp.utils.getNodeById(nodeId, self.graph)

        self.assertTrue(node)

    def test_getNodeTypes(self):

        # Case where there is a node label.
        nodeType = 'CBb3-4i'
        nodes = tp.utils.getNodesByType(nodeType, self.graph)

        self.assertTrue(len(nodes) == 1)

        foundType = tp.utils.getNodeType(nodes[0], self.graph)

        self.assertTrue(foundType == nodeType)

        # Case with no node label
        nodeId = 606
        node = tp.utils.getNodeById(nodeId, self.graph)
        foundType = tp.utils.getNodeType(node, self.graph)

        self.assertTrue(foundType == 'null')