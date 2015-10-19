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

        stats = tp.PathStats(finder.valid)

        # Tests of unique path counting
        self.assertTrue(stats.getNumPathsWithLoop() == 2)
        self.assertTrue(stats.getNumUniqueTypes() == 4)
        self.assertTrue(stats.getNumPaths() == len(finder.valid))

    def test_intermediateStatCounting(self):
        graphFile = '../data/test_two.tlp'
        sourceId = 5860
        targetId = 606
        maxNumHops = 2

        graph = tlp.loadGraph(graphFile)
        sourceNode = tp.getNodeById(sourceId, graph)
        targetNode = tp.getNodeById(targetId, graph)

        finder = tp.PathFinder(graph)
        finder.findPaths(sourceNode, targetNode, maxNumHops)

        stats = tp.PathStats(finder.valid)

        self.assertTrue(stats.getNumPathsWithLoop() == 0)
        self.assertTrue(stats.getNumPaths() == len(finder.valid))
        self.assertTrue(stats.getNumUniqueTypes() == 2)

        unique = stats.getUniqueTypes()
        self.assertTrue(unique[0].toStringOfTypes() == 'GAC Aii, Gap Junction, CBb3-4i, Ribbon Synapse, GC ON')
        self.assertTrue(unique[1].toStringOfTypes() == 'GAC Aii, Gap Junction, CBb4w, Ribbon Synapse, GC ON')

