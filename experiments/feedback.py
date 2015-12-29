"""
    This is an experiment of searching for feedback in ACs.
"""

from tulip import *
from tulipgui import *
import tulippaths as tp

# Load the graph.
graph = tlp.loadGraph("../data/514_4hops.tlp")

nodes = tp.utils.getNodesByTypes(['YAC', 'AC', 'IAC'], graph)
ffNodeTypes = ['GC', 'GC ON', 'GC ON/OFF', 'GC direction', 'GC direction selective', 'GC fragment', 'GC?', 'GC diving', 'GC OFF']
fbNodeTypes = ['CBb3m', 'CBb5w', 'CBb4w', 'CBb3-4i', 'CBb6', 'CBb5i','CBb','CBb [G+]', 'CBb5-6i', 'CBb4i', 'CBb5', 'CBb6i', 'CBb4-5i', 'CBb3-4-5i', 'CBb3', 'CBb4-5-6i', 'CBb4iw', 'CBb3i', 'CBb4', 'CBb3-4', 'CBbw', 'CBbx', 'CBb3w [:: CBb3']

print 'id, nodeType, isFeedback, isFeedforward'
numNeither = 0
numNotSkipped = 0
for node in nodes:

    if tp.utils.getApproximateNumAnnotations(node, graph) == 2:
       continue

    numNotSkipped += 1
    canBeReachedFromCBb = tp.utils.canBeReachedFromTypes(node, fbNodeTypes, graph)
    canReachCBb = tp.utils.canReachTypes(node, fbNodeTypes, graph)
    canReachGC = tp.utils.canReachTypes(node, ffNodeTypes, graph)
    #print tp.utils.getNodeId(node, graph)
    isFeedbackNode = canBeReachedFromCBb and canReachGC
    isFeedForwardNode = canBeReachedFromCBb and canReachCBb

    id = tp.utils.getNodeId(node, graph)
    nodeType = tp.utils.getNodeType(node, graph)



    if isFeedbackNode or isFeedForwardNode:
        print id + ', ' + nodeType + ', ' + str(isFeedbackNode) + ', ' + str(isFeedForwardNode)
    else:
        numNeither += 1



print 'percent skipped ' + str((len(nodes) - numNotSkipped) / float(len(nodes)))
print 'percent neither ff nor fb: '  + str(numNeither / float(numNotSkipped))


# Render the graph in a node-link diagram.
nodeLinkView = tlpgui.createNodeLinkDiagramView(graph)

