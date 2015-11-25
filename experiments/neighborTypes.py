""" Trying to get an idea for scale of neighbor types """
from tulip import *
from tulipgui import *
import tulippaths as tp

# Path parameters
graphFile = '../data/514_4hops.tlp'
graph = tlp.loadGraph(graphFile)
label = 'CBb5w'
nodes = tp.utils.getNodesByType('CBb5w', graph)

def getUniqueLabels(nodes, graph):
    uniqueLabels = []
    for node in nodes:
        label = tp.utils.getNodeType(node, graph)
        if label not in uniqueLabels:
            uniqueLabels.append(label)
    return uniqueLabels

showCompleteness = True
completeness = {}
if showCompleteness:
    completeness = tp.utils.getApproximateAnnotationCompleteness(graph)

output = open('test1.csv', 'w')

labels = ['CBb5w', 'CBb4w']
connections = ['Gap Junction', 'Conventional', 'Ribbon Synapse', 'Adherens', 'BC Conventional Synapse', 'Touch', 'Unknown']
items = ['label', 'id', '%complete', 'labels (G)','labels (CS)','labels (R)','labels (A)','labels (BCS)', 'labels (T)', 'labels (U)', 'ngbrs (G)','ngbrs (CS)','ngbrs (R)','ngbrs (A)','ngbrs (BCS)', 'ngbrs (T)', 'ngbrs (U)']
header = ''

# Write the header to the file.
for item in items:
    header += '{0:15},'.format(item)
print header
output.write(header + '\n')

for label in labels:
    nodes = tp.utils.getNodesByType(label, graph)
    for node in nodes:

        neighbors = {}
        neighborWeights = {}

        for c in connections:
            neighbors[c] = []
            neighborWeights[c] = []

        for edge in graph.getInOutEdges(node):
            other = graph.target(edge)
            if other == node:
                other = graph.source(edge)
            edgeType = tp.utils.getEdgeType(edge, graph)
            edgeWeight = tp.utils.getEdgeWeight(edge, graph)

            if edgeType not in connections:
                print 'skipping edgeType: ' + edgeType
                continue
            else:
                neighbors[edgeType].append(other)
                neighborWeights[edgeType].append(edgeWeight)

        numNeighborsByEdgeType = []
        numLabelsByEdgeType = []
        for child in connections:
            numNeighborsByEdgeType.append(len(neighbors[child]))
            removed = list(set(neighbors[child]))
            print str(len(removed)) + ', ' + str(len(neighbors[child]))
            numLabelsByEdgeType.append(len(getUniqueLabels(neighbors[child], graph)))

        attributes = [label, tp.getNodeId(node, graph), '{0:0.3f}'.format(completeness[node])] + numLabelsByEdgeType + numNeighborsByEdgeType
        line = ''
        for attribute in attributes:
            line += '{0:15},'.format(attribute)
        output.write(line)
        output.write('\n')

output.close()

