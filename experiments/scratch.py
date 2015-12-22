""" Scratch work to get info about one node. """
from tulip import *
from tulipgui import *
import tulippaths as tp

showCompleteness = True

# Path parameters
graphFile = '../data/514_476_10hops.tlp'
graph = tlp.loadGraph(graphFile)

def getUniqueLabels(nodes, graph):
    uniqueLabels = []
    for node in nodes:
        label = tp.utils.getNodeType(node, graph)
        if label not in uniqueLabels:
            uniqueLabels.append(label)
    return uniqueLabels

completeness = {}

if showCompleteness:
    completeness = tp.utils.getApproximateAnnotationCompleteness(graph)

node = tp.utils.getNodeById(593, graph)

neighborLabels = {}
for edge in graph.getOutEdges(593):
    target = graph.target(edge)
    print tp.utils.getEdgeType(edge, graph)

    
