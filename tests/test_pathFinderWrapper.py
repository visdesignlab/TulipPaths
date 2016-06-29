from unittest import TestCase
from tulip import *
import tulippaths as tp

class TestPathFinderWrapper(TestCase):

    def test_findRegexConstrainedPaths(self):
        graphFile = '../data/test_one.tlp'
        graph = tlp.loadGraph(graphFile)

        edgeConstraints = ["Ribbon Synapse", "Adherens"]
        nodeConstraints = ["CBb3-4i", "GC ON", "CBb4w"]

        pathFinderWrapper = tp.PathFinderWrapper(graph)

        paths = pathFinderWrapper.findRegexConstrainedPaths(nodeConstraints, edgeConstraints)

        path = paths[0]

        self.assertTrue(path.toStringOfTypes() == "CBb3-4i, Ribbon Synapse, GC ON, Adherens, CBb4w")
        self.assertTrue(path.toStringOfIds() == "176, (53563 -> 53564    53563 -> 53564), 606, (54048 -> 54049    54050 -> 54051    82555 -> 80970    82684 -> 77469    82882 -> 81107    82885 -> 81135), 5530")
