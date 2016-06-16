import unittest
from unittest import TestCase
from tulip import *
import tulippaths as tp
import json


class TestConnectivityMatrix(TestCase):
    def setUp(self):
        graphFile = '../data/test_feedback.tlp'
        self.graph = tlp.loadGraph(graphFile)
        acRegexes = ['AC', 'IAC', 'YAC']
        acRegexes = '(?:%s)' % '|'.join(acRegexes)
        nodeConstraints = ['CBb.*', acRegexes, 'GC']
        edgeConstraints = ['.*', '.*']

        self.matrix = tp.ConnectivityMatrix(self.graph)
        self.matrix.activate(nodeConstraints, edgeConstraints)

    def assertOutputMatches(self, matrix, removeUnused, string):
        self.assertTrue(json.dumps(matrix.getAsJsonObject(removeUnused)) == string)

    # The connectivity matrix should find two paths in this test.
    def test_activate(self):
        matrix = self.matrix
        self.assertTrue(len(matrix._matrix) == 5)
        for i in range(0, len(matrix._matrix)):
            row = matrix._matrix[i]
            self.assertTrue(len(row) == 5)
            if i == 1:
                self.assertTrue(len(row[4]) == 1)
                self.assertTrue(
                        matrix.getPathAt(row[4][0]).toStringOfTypes() == 'CBb3m, Ribbon Synapse, IAC, Conventional, GC')
            elif i == 3:
                self.assertTrue(len(row[2]) == 1)
                self.assertTrue(
                        matrix.getPathAt(row[2][0]).toStringOfTypes() == 'CBb3m, Ribbon Synapse, YAC, Conventional, GC')
            else:
                for col in row:
                    self.assertTrue(len(col) == 0)

    # Json object format is meant to be input into reorder.js
    def test_getAsJsonObject(self):
        removeUnusedNodes = False
        self.assertOutputMatches(self.matrix,
                                 removeUnusedNodes,
                                 '{"row_labels": ["168", "120", "142", "1724", "5107"], '
                                 '"matrix": [[[], [], [], [], []], [[], [], [], [], [[2, 3, 4, 4, 6]]], [[], [], [], [], []], [[], [], [[5, 1, 1, 6, 3]], [], []], [[], [], [], [], []]], '
                                 '"col_labels": ["168", "120", "142", "1724", "5107"]}')

        removeUnusedNodes = True
        self.assertOutputMatches(self.matrix,
                                 removeUnusedNodes,
                                 '{"row_labels": ["120", "1724"], '
                                 '"matrix": [[[[2, 3, 4, 4, 6]], []], [[], [[5, 1, 1, 6, 3]]]], '
                                 '"col_labels": ["5107", "142"]}')

    # Collapse sources and targets of connectivity matrix by their node type!
    def test_collapseSourcesAndTargets(self):
        removeUnusedNodes = False
        self.matrix.collapseSources()
        self.assertOutputMatches(self.matrix,
                                 removeUnusedNodes,
                                 '{"row_labels": ["CBb3m", "GC"], '
                                 '"matrix": [[[], [], [[5, 1, 1, 6, 3]], [], [[2, 3, 4, 4, 6]]], [[], [], [], [], []]], '
                                 '"col_labels": ["168", "120", "142", "1724", "5107"]}')

        removeUnusedNodes = True
        self.assertOutputMatches(self.matrix,
                                 removeUnusedNodes,
                                 '{"row_labels": ["CBb3m"], '
                                 '"matrix": [[[[5, 1, 1, 6, 3]], [[2, 3, 4, 4, 6]]]], '
                                 '"col_labels": ["142", "5107"]}')

        self.matrix.reset()
        self.matrix.collapseTargets()
        removeUnusedNodes = False
        self.assertOutputMatches(self.matrix,
                                 removeUnusedNodes,
                                 '{"row_labels": ["168", "120", "142", "1724", "5107"], '
                                 '"matrix": [[[], []], [[], [[2, 3, 4, 4, 6]]], [[], []], [[], [[5, 1, 1, 6, 3]]], [[], []]], '
                                 '"col_labels": ["CBb3m", "GC"]}')

if __name__ == "__main__":
    unittest.main()
