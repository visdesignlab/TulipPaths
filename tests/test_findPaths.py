from unittest import TestCase
from tulip import *
import TulipPaths as tp

class TestFindPaths(TestCase):

    def test_findPath(self):
        file = '../data/test_zero.tlp'
        graph = tlp.loadGraph(file)
        sourceId = 176
        targetId = 606
        maxNumHops = 1

        sourceNode = tp.getNodeById(sourceId, graph)
        targetNode = tp.getNodeById(targetId, graph)

        results = tp.findPaths(sourceNode, targetNode, maxNumHops, graph)

        self.assertTrue(len(results[tp.VALID_PATHS]) == 1)
        self.assertTrue(results[tp.VALID_PATHS][0].isSane())
        self.assertTrue(len(results[tp.FAILED_PATHS]) == 0)