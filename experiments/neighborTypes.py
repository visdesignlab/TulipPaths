""" Trying to get an idea for scale of neighbor types """
from tulip import *
from tulipgui import *
import tulippaths as tp

showCompleteness = True

# Path parameters
graphFile = '../data/514_476_10hops.tlp'
graph = tlp.loadGraph(graphFile)


completeness = {}
if showCompleteness:
    completeness = tp.utils.getApproximateAnnotationCompleteness(graph)
    #for node in nodes:
        #print str(node) + ', ' + str(completeness[node])

labels = ['GAC Aii', 'CBb5w']
for label in labels:
    print '==== Label' + label + '====='


    print '{0:10}, {1:10}, {2:10}, {3:10}, {4:10}, {5:10}'.format('node', '%complete', 'ngbr labels', 'unique ngbrs', '2-hop nbrs', 'unique 2-hop')
    nodes = tp.utils.getNodesByType(label, graph)
    for node in nodes:

        if completeness[node] < 0.25:
            continue

        neighbors = {}
        uniqueNeighbors = []
        for edge in graph.getInOutEdges(node):
            other = graph.target(edge)
            label = tp.utils.getNodeType(other, graph)
            if label in neighbors:
                neighbors[label] += 1
            else:
                neighbors[label] = 1
            if not other in uniqueNeighbors:
                uniqueNeighbors.append(other)

        neighborsNeighbors = {}
        uniqueNeighborsNeighbors = []
        for neighbor in uniqueNeighbors:
            for edge in graph.getInOutEdges(neighbor):
                other = graph.target(edge)
                label = tp.utils.getNodeType(other, graph)
                if label in neighborsNeighbors:
                    neighborsNeighbors[label] += 1
                else:
                    neighborsNeighbors[label] = 1
                if not other in uniqueNeighborsNeighbors:
                    uniqueNeighborsNeighbors.append(other)


        print '{0:10}, {1:10}, {2:10}, {3:10}, {4:10}, {5:10}'.format(node, '{0:0.3f}'.format(completeness[node]), (len(neighbors.values())), (len(uniqueNeighbors)), len(neighborsNeighbors.values()), len(uniqueNeighborsNeighbors))

