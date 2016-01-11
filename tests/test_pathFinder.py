import unittest
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

    # TODO this test appears to be ineffective because the PathFinder
    # finds no paths for some reason
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

        for path in pathFinder.valid:
            self.assertTrue(path.isInTypeConstraints(constrainedToEdgeTypes,
                                                     constrainedToNodeTypes))

    # TODO this test appears to be ineffective because the PathFinder
    # finds no paths for some reason
    def test_findRegexConstrainedPaths(self):
        graphFile = '../data/test_one.tlp'
        graph = tlp.loadGraph(graphFile)
        tp.VERBOSE = True
        source = tp.utils.getNodeById(176, graph)
        target = tp.utils.getNodeById(5530, graph)

        constrainedToEdgeTypeRegexes = [".+ Synapse", "^Adhe.+$"]
        constrainedToNodeTypeRegexes = ["CBb3-.+$", "^GC [ON|OFF]$", "[A-Z]Bb4w"]

        pathFinder = tp.PathFinder(graph)

        pathFinder.findRegexConstrainedPaths(source,
                                             constrainedToEdgeTypeRegexes,
                                             constrainedToNodeTypeRegexes)

        for path in pathFinder.valid:
            self.assertTrue(path.isInRegexTypeConstraints(
                constrainedToEdgeTypeRegexes, constrainedToNodeTypeRegexes))


if __name__ == "__main__":
    unittest.main()
