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

    # The connectivity matrix should find two paths in this test.
    def test_activate(self):
        matrix = self.matrix
        self.assertTrue(len(matrix._matrix) == 5)
        for i in range(0, len(matrix._matrix)):
            row = matrix._matrix[i]
            self.assertTrue(len(row) == 5)
            if i == 1:
                self.assertTrue(len(row[4]) == 1)
                self.assertTrue(row[4][0].toStringOfTypes() == 'CBb3m, Ribbon Synapse, IAC, Conventional, GC')
            elif i == 3:
                self.assertTrue(len(row[2]) == 1)
                self.assertTrue(row[2][0].toStringOfTypes() == 'CBb3m, Ribbon Synapse, YAC, Conventional, GC')
            else:
                for col in row:
                    self.assertTrue(len(col) == 0)

    def test_getPathCountJsonMatrix(self):
        matrix = self.matrix
        jsonObject = matrix.getPathCountJsonMatrix()
        self.assertTrue(json.dumps(jsonObject) == '{"row_labels": ["168", "120", "142", "1724", "5107"], "matrix": [[0, 0, 0, 0, 0], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0]], "col_labels": ["168", "120", "142", "1724", "5107"]}')

if __name__ == "__main__":
    unittest.main()
