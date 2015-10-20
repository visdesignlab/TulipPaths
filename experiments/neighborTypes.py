""" Trying to get an idea for scale of neighbor types """
from tulip import *
from tulipgui import *
import tulippaths as tp

showCompleteness = False

# Path parameters
graphFile = '../data/514_4hops.tlp'
graph = tlp.loadGraph(graphFile)
label = 'CBb5w'
nodes = tp.utils.getNodesByType('CBb5w', graph)

if showCompleteness:
    completeness = tp.utils.getApproximateAnnotationCompleteness(graph)
    for node in nodes:
        print str(node) + ', ' + str(completeness[node])

for node in nodes:
    print 'neighbors of node: ' + str(node)
    neighbors = {}
    for edge in graph.getInOutEdges(node):
        other = graph.target(edge)
        label = tp.utils.getNodeType(other, graph)
        if label in neighbors:
            neighbors[label] += 1
        else:
            neighbors[label] = 1
    print neighbors