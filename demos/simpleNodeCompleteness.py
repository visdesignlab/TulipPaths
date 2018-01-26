""" Example of reasoning about the approximate node completeness. """

from tulip import *
from tulipgui import *
import tulippaths as tp

# Load graph
graphFile = '../data/514_4hops.tlp'
graph = tlp.loadGraph(graphFile)

# Compute completeness for each node label
completeness = tp.utils.getApproximateAnnotationCompleteness(graph)

# Tally completeness
numComplete = 0
numAlmostComplete = 0
numIncomplete = 0
for node in graph.getNodes():
    currCompleteness = completeness[node]
    if currCompleteness <= 1.0 and currCompleteness > 0.75:
        numComplete += 1
    elif currCompleteness <= 0.75 and currCompleteness > 0.25:
        numAlmostComplete += 1
    else:
        graph.delNode(node)
        numIncomplete += 1

print('num complete, num almost complete, num incomplete')
print((str(numComplete) + ', ' + str(numAlmostComplete) + ', ' + str(numIncomplete)))

nodeLinkView = tlpgui.createNodeLinkDiagramView(graph)