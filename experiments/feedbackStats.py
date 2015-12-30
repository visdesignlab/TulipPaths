from tulip import *
from tulipgui import *
import tulippaths as tp

graphFile = '../data/514_4hops.tlp'
graph = tlp.loadGraph(graphFile)
percentCompletenessThreshold = 0.2

completeness = tp.utils.getApproximateAnnotationCompleteness(graph)

superTypeDictionary = tp.SuperTypeDictionary()

nodeTypes = superTypeDictionary.getTypesFromSuperTypes(['YAC', 'GAC'])

allACNodes = tp.utils.getNodesByTypes(nodeTypes, graph)
print 'Total num nodes with super-label yac and gac: ' + str(len(allACNodes))

acNodes = []

for node in allACNodes:
    if completeness[node] > percentCompletenessThreshold:
        acNodes.append(node)

print 'Num nodes complete enough for analysis: ' + str(len(acNodes))


ffNodeTypes = superTypeDictionary.getTypesFromSuperTypes(['GC'])
fbNodeTypes = superTypeDictionary.getTypesFromSuperType('CBb')

print 'id, nodeType, isFeedback, isFeedforward'
numNeither = 0
numNotSkipped = 0
for node in acNodes:

    numNotSkipped += 1
    canBeReachedFromCBb = tp.utils.canBeReachedFromTypes(node, fbNodeTypes, graph)
    canReachCBb = tp.utils.canReachTypes(node, fbNodeTypes, graph)
    canReachGC = tp.utils.canReachTypes(node, ffNodeTypes, graph)

    isFeedbackNode = canBeReachedFromCBb and canReachCBb
    isFeedForwardNode = canBeReachedFromCBb and canReachGC

    id = tp.utils.getNodeId(node, graph)
    nodeType = tp.utils.getNodeType(node, graph)

    if isFeedbackNode or isFeedForwardNode:
        print id + ', ' + nodeType + ', ' + str(isFeedbackNode) + ', ' + str(isFeedForwardNode)
    else:
        numNeither += 1


print 'percent neither ff nor fb: '  + str(numNeither / float(numNotSkipped))

# Render the graph in a node-link diagram.
nodeLinkView = tlpgui.createNodeLinkDiagramView(graph)


