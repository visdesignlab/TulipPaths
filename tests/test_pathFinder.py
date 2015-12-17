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

        finder = tp.PathFinder(graph)
        finder.findPaths(sourceNode, targetNode, maxNumHops)

        self.assertTrue(len(finder.valid) == 1)
        self.assertTrue(finder.valid[0].isSane())
        self.assertTrue(len(finder.failed) == 0)

    def test_findPathOne(self):
        tp.VERBOSE = True
        graphFile = '../data/test_one.tlp'
        sourceId = 176
        targetId = 606
        maxNumHops = 4

        graph = tlp.loadGraph(graphFile)
        sourceNode = tp.getNodeById(sourceId, graph)
        targetNode = tp.getNodeById(targetId, graph)

        finder = tp.PathFinder(graph)
        finder.findPaths(sourceNode, targetNode, maxNumHops)

        self.assertTrue(len(finder.valid) == 4)
        self.assertTrue(len(finder.failed) == 1)
        for path in finder.valid:
            self.assertTrue(path.isSane())

    def test_findAllPaths(self):
        tp.VERBOSE = True
        graphFile = '../data/test_one.tlp'
        maxNumHops = 2
        sourceId = 176

        graph = tlp.loadGraph(graphFile)

        sourceNode = tp.getNodeById(sourceId, graph)

        finder = tp.PathFinder(graph)
        finder.findAllPaths(sourceNode, maxNumHops)

        self.assertTrue(len(finder.valid) == 3)

    def test_findConstrainedPaths(self):
        graphFile = '../data/test_one.tlp'
        graph = tlp.loadGraph(graphFile)
        tp.VERBOSE = True
        source = tp.utils.getNodeById(176, graph)
        target = tp.utils.getNodeById(5530, graph)

        constrainedToEdgeTypes = ["Ribbon Synapse", "Adherens"]
        constrainedToNodeTypes = ["CBb3-4i", "GC ON", "CBb4w"]

        pathFinder = tp.PathFinder(graph)

        pathFinder.findConstrainedPaths(source, constrainedToEdgeTypes, constrainedToNodeTypes)
        print len(pathFinder.valid)
        for path in pathFinder.valid:
            print path.toStringOfTypes()