from unittest import TestCase
from tulip import *
import tulippaths as tp

class TestFindPaths(TestCase):

    def test_findPathZero(self):
        graphFile = '../data/test_zero.tlp'
        graph = tlp.loadGraph(graphFile)
        sourceId = 176
        targetId = 606
        maxNumHops = 1

        sourceNode = tp.getNodeById(sourceId, graph)
        targetNode = tp.getNodeById(targetId, graph)

        results = tp.findPaths(sourceNode, targetNode, maxNumHops, graph)

        self.assertTrue(len(results[tp.VALID_PATHS]) == 1)
        self.assertTrue(results[tp.VALID_PATHS][0].isSane())
        self.assertTrue(len(results[tp.FAILED_PATHS]) == 0)

    def test_findPathOne(self):
        tp.VERBOSE = True
        graphFile = '../data/test_one.tlp'
        sourceId = 176
        targetId = 606
        maxNumHops = 4

        graph = tlp.loadGraph(graphFile)
        sourceNode = tp.getNodeById(sourceId, graph)
        targetNode = tp.getNodeById(targetId, graph)

        results = tp.findPaths(sourceNode, targetNode, maxNumHops, graph)
        valid = results[tp.VALID_PATHS]
        failed = results[tp.FAILED_PATHS]

        self.assertTrue(len(valid) == 4)
        self.assertTrue(len(failed) == 1)
        for path in valid:
            self.assertTrue(path.isSane())