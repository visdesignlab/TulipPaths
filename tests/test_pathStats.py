from unittest import TestCase
from tulip import *
import tulippaths as tp

class TestPathStats(TestCase):

    def test_basicStatCounting(self):
        graphFile = '../data/test_one.tlp'
        sourceId = 176
        targetId = 606
        maxNumHops = 4

        graph = tlp.loadGraph(graphFile)
        sourceNode = tp.getNodeById(sourceId, graph)
        targetNode = tp.getNodeById(targetId, graph)

        finder = tp.PathFinder(graph)
        finder.findPaths(sourceNode, targetNode, maxNumHops)

        for path in finder.valid:
            print path.toString()
            print path.toStringOfTypes()

        stats = tp.PathStats(finder.valid)

        # Tests of unique path counting
        self.assertTrue(stats.getNumPathsWithLoop() == 2)
        self.assertTrue(stats.getNumPathsWithStartLoop() == 1)
        self.assertTrue(stats.getNumUniqueTypes() == 4)

        # Tests of unique types


