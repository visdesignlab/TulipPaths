import unittest
from unittest import TestCase

from tulip import *
import tulippaths as tp


class TestUtils(TestCase):
    def test_graphToJson(self):
        file = '../data/test_two.tlp'
        graph = tlp.loadGraph(file)
        graphJson = tp.export.graphToJson(graph)

        self.assertTrue(len(graphJson['nodes']) == 5)

        for node in graphJson['nodes']:
            self.assertTrue(tp.utils.getNodeById(node['StructureID'], graph).id == node['ID'])

        self.assertTrue(len(graphJson['edges']) == 13)

        for edge in graphJson['edges']:
            source = tp.utils.getNodeById(edge['SourceStructureID'], graph)
            target = tp.utils.getNodeById(edge['TargetStructureID'], graph)
            self.assertTrue(graph.existEdge(source, target))


if __name__ == "__main__":
    unittest.main()
