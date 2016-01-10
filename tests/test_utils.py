import unittest
from unittest import TestCase

from tulip import *
import tulippaths as tp

import re

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

    def test_getAllEdgeTypes(self):
        self.file = '../data/test_one.tlp'
        self.graph = tlp.loadGraph(self.file)
        edgeTypes = tp.utils.getAllEdgeTypes(self.graph)
        self.assertTrue(edgeTypes == ['Touch', 'Ribbon Synapse', 'Unknown', 'Adherens', 'Gap Junction'])

    def test_getDictionaryOfEdgeTypes(self):
        self.file = '../data/test_two.tlp'
        self.graph = tlp.loadGraph(self.file)
        dictionary = tp.utils.getDictionaryOfEdgeTypes(self.graph)

        for key in dictionary.keys():
            values = dictionary[key]
            for edge in values:
                self.assertTrue(tp.utils.getEdgeType(edge, self.graph) == key)

    def test_getDictionaryOfNodeTypes(self):
        self.file = '../data/test_two.tlp'
        self.graph = tlp.loadGraph(self.file)

        dictionary = tp.utils.getDictionaryOfNodeTypes(self.graph)

        for key in dictionary.keys():
            values = dictionary[key]
            for node in values:
                self.assertTrue(tp.utils.getNodeType(node, self.graph) == key)

    def test_isEdgeTypeInGraph(self):
        self.file = '../data/test_two.tlp'
        self.graph = tlp.loadGraph(self.file)

        self.assertTrue(tp.utils.isEdgeTypeInGraph('Gap Junction', self.graph))
        self.assertFalse(tp.utils.isEdgeTypeInGraph('Gap Junctionf', self.graph))

    def test_canBeReachedFrom(self):
        self.file = '../data/test_two.tlp'
        graph = tlp.loadGraph(self.file)

        # Node of cell id 1 should be reachable from GAC Aii label
        source = tp.utils.getNodeById(1, graph)
        self.assertTrue(len(tp.utils.canBeReachedFromTypes(source, ['GAC Aii'], graph)) == 1)

        # Node of cell id 5860 should be able to reach CBb3-4i (cell id #1)
        source = tp.utils.getNodeById(5860, graph)
        self.assertTrue(len(tp.utils.canReachTypes(source, ['CBb3-4i'], graph)))

        source = tp.utils.getNodeById(606, graph)
        self.assertTrue(len(tp.utils.canReachTypes(source, ['CBb3-4i'], graph)) == 0)
        self.assertTrue(len(tp.utils.canBeReachedFromTypes(source, ['GAC Aii'], graph)) == 0)

    def test_getNodesByType(self):
        self.file = '../data/test_two.tlp'

        graph = tlp.loadGraph(self.file)
        nodes = tp.utils.getNodesByType('GAC Aii', graph)

        self.assertTrue(len(nodes) == 1)
        self.assertTrue(tp.utils.getNodeType(nodes[0], graph) == 'GAC Aii')

    def test_getNodesByTypes(self):
        self.file = '../data/test_two.tlp'

        graph = tlp.loadGraph(self.file)

        nodeTypes = ['GAC Aii', 'CBb3-4i']
        nodes = tp.utils.getNodesByTypes(nodeTypes, graph)

        self.assertTrue(len(nodes) == 3)

        for node in nodes:
            self.assertTrue(tp.utils.getNodeType(node, graph) in nodeTypes)

    def test_getNodesByTypeRegex(self):
        self.file = '../data/test_two.tlp'

        # Test multiple cases by looping through this dictionary.
        # "regex": num_nodes
        test_cases = {
            "^$": 0,
            "^GAC Aii$": 1,
            "^GC ON$": 1,
            "^CBb3-4i$": 2,
            "^CBb4w$": 1,
            "^GA?C.*$": 2,
            "^CBb.*$": 3
        }

        graph = tlp.loadGraph(self.file)

        for test_regex, expected_results in test_cases.iteritems():
            nodes = tp.utils.getNodesByTypeRegex(test_regex, graph)

            self.assertTrue(len(nodes) == expected_results)
            for node in nodes:
                self.assertTrue(
                    re.search(re.compile(test_regex),
                              tp.utils.getNodeType(node, graph)))

    def test_getNodesByTypeRegexes(self):
        self.file = '../data/test_two.tlp'

        graph = tlp.loadGraph(self.file)

        # Test multiple cases by looping through this dictionary.
        # "regex,other_regex": num_nodes
        test_cases = {
            "^GAC Aii$,^CBb3-4i$": 3,
            "^GA?C.*$,^CBb3-4i$": 4
        }

        for test_regex_list, expected_results in test_cases.iteritems():
            nodeTypeRegexes = test_regex_list.split(',')
            nodes = tp.utils.getNodesByTypeRegexes(nodeTypeRegexes, graph)

            self.assertTrue(len(nodes) == expected_results)


if __name__ == "__main__":
    unittest.main()
