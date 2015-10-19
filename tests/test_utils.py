from unittest import TestCase

from tulip import *
import tulippaths as tp

class TestUtils(TestCase):

    def setUp(self):
        self.file = '../data/test_zero.tlp'
        self.graph = tlp.loadGraph(self.file)

    def test_getEdgeType(self):
        edgeType = 0

        for edge in self.graph.getEdges():
            edgeType = tp.utils.getEdgeType(edge, self.graph)

        self.assertTrue(edgeType == 'Ribbon Synapse')

    def test_getEdgeWeight(self):
        for edge in self.graph.getEdges():
            self.assertTrue(tp.utils.getEdgeWeight(edge, self.graph) == 2)

    def test_getApproximateNumAnnotationsZero(self):
        nodeId = 606
        node = tp.utils.getNodeById(nodeId, self.graph)
        self.assertTrue(tp.getApproximateNumAnnotations(node, self.graph) == 2)

    def test_getApproximateNumAnnotationsOne(self):
        self.file = '../data/test_one.tlp'
        self.graph = tlp.loadGraph(self.file)

        nodeId = 176
        expectedNumAnnotations = 9
        node = tp.utils.getNodeById(nodeId, self.graph)
        self.assertTrue(tp.getApproximateNumAnnotations(node, self.graph) == expectedNumAnnotations)

        nodeId = 606
        expectedNumAnnotations = 34
        node = tp.utils.getNodeById(nodeId, self.graph)
        self.assertTrue(tp.getApproximateNumAnnotations(node, self.graph) == expectedNumAnnotations)

        nodeId = 5530
        expectedNumAnnotations = 59
        node = tp.utils.getNodeById(nodeId, self.graph)
        self.assertTrue(tp.getApproximateNumAnnotations(node, self.graph) == expectedNumAnnotations)

    def test_getApproximateAnnotationCompletenessOne(self):
        self.file = '../data/test_one.tlp'
        self.graph = tlp.loadGraph(self.file)
        completeness = tp.utils.getApproximateAnnotationCompleteness(self.graph)

        for node in self.graph.getNodes():
            self.assertTrue(completeness[node] == 1.0)

    def test_getApproximateAnnotationCompletenessTwo(self):
        self.file = '../data/test_two.tlp'
        self.graph = tlp.loadGraph(self.file)

        # Nodes 176, 606, and 5530 are the most annotated nodes in their labels and should be 100% annotated.
        # Node 1 only has 2 children annotations compared to node 5530's 16 annotations.
        # 2 annotations / 16 annotations  => 0.125 percent complete.
        nodeIds = [176, 606, 5530, 1]
        expectedCompleteness = [1.0, 1.0, 1.0, 0.125]

        completeness = tp.utils.getApproximateAnnotationCompleteness(self.graph)
        for i in range(0, len(nodeIds)):
            node = tp.utils.getNodeById(nodeIds[i], self.graph)
            self.assertTrue(completeness[node] == expectedCompleteness[i])