from unittest import TestCase
from tulip import *
import tulippaths as tp

class TestPathTracker(TestCase):

    def test_pathTracker(self):
        tp.VERBOSE = True
        graphFile = '../data/test_one.tlp'
        maxNumHops = 2
        sourceId = 176

        graph = tlp.loadGraph(graphFile)

        sourceNode = tp.getNodeById(sourceId, graph)

        finder = tp.PathFinder(graph)
        finder.findAllPaths(sourceNode, maxNumHops)

        tracker = tp.PathTracker()
        for path in finder.valid:
            tracker.getOrCreatePathTypeID(path)

        self.assertTrue(tracker.getNumUniquePathTypes() == 3)

        for i in range(0, len(finder.valid)):
            self.assertTrue(tracker.getOrCreatePathTypeID(finder.valid[i]) == i)



