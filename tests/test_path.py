from unittest import TestCase
from tulip import *
import TulipPaths as tp


class TestPath(TestCase):

    def setUp(self):
        graphFile = '../data/test_one.tlp'
        self.graph = tlp.loadGraph(graphFile)
        self.startNodeId = 606

    def test_addNode(self):

        path = tp.Path(self.graph)
        node = tp.getNodeById(self.startNodeId, self.graph)
        path.addNode(node)

        self.assertTrue(len(path.nodes) == 1)
        self.assertTrue(path.nodes[0] == node)
        self.assertTrue(path.isSane())

    def test_addEdge(self):

        path = tp.Path(self.graph)
        node = tp.getNodeById(self.startNodeId, self.graph)
        path.addNode(node)

        edges = self.graph.getOutEdges(node)

        for edge in edges:
            path.addEdge(edge)
            path.addNode(self.graph.target(edge))
            break

        self.assertTrue(len(path.edges) == 1)
        self.assertTrue(len(path.nodes) == 2)
        self.assertTrue(path.isSane())

    def test_getLastNode(self):

        path = tp.Path(self.graph)
        node = tp.getNodeById(self.startNodeId, self.graph)
        path.addNode(node)

        edges = self.graph.getOutEdges(node)
        lastNode = 0
        for edge in edges:
            path.addEdge(edge)
            lastNode = self.graph.target(edge)
            path.addNode(lastNode)
            break

        self.assertTrue(path.getLastNode() == lastNode)
        self.assertTrue(path.isSane())

    def test_isSameType(self):
        self.fail()

    def test_size(self):
        self.fail()

    def test_toString(self):
        self.fail()

    def test_toStringOfTypes(self):
        self.fail()
