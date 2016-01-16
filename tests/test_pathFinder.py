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
        source = tp.utils.getNodeById(176, graph)

        edgeConstraints = ["Ribbon Synapse", "Adherens"]
        nodeConstraints = ["CBb3-4i", "GC ON", "CBb4w"]

        pathFinder = tp.PathFinder(graph)

        pathFinder.findConstrainedPaths(source, edgeConstraints, nodeConstraints)

        self.assertTrue(len(pathFinder.valid) == 1)

        for path in pathFinder.valid:
            self.assertTrue(path.isInTypeConstraints(edgeConstraints,
                                                     nodeConstraints))

    def test_findRegexConstrainedPaths(self):
        graphFile = '../data/test_two.tlp'
        graph = tlp.loadGraph(graphFile)
        source = tp.utils.getNodeById(176, graph)

        edgeConstraintRegexes = [".+ Synapse", "^Adhe.+$"]
        nodeConstraintRegexes = ["CBb3-.+$", "^GC ON", "[A-Z]Bb4w"]

        pathFinder = tp.PathFinder(graph)

        pathFinder.findRegexConstrainedPaths(source, edgeConstraintRegexes, nodeConstraintRegexes)

        self.assertTrue(len(pathFinder.valid) == 1)

        for path in pathFinder.valid:
            self.assertTrue(path.isInRegexTypeConstraints(edgeConstraintRegexes, nodeConstraintRegexes))


if __name__ == "__main__":
    unittest.main()
