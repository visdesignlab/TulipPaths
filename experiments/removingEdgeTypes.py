""" Trying to remove edge types..."""

from tulip import *
from tulipgui import *
import tulippaths as tp

graphFile = '../data/514_476_10hops.tlp'
graph = tlp.loadGraph(graphFile)

for edge in graph.getEdges():
    if tp.utils.getEdgeType(edge, graph) != 'Gap Junction':
        graph.delEdge(edge)

for edge in graph.getEdges():
    tp.utils.setColor(edge, tlp.Color.Black, graph)

for node in graph.getNodes():
    if graph.deg(node) == 0:
        graph.delNode(node)
nodeLinkView = tlpgui.createNodeLinkDiagramView(graph)