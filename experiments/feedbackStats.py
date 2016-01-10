from tulip import *
from tulipgui import *
import tulippaths as tp

graphFile = '../data/514_10hops_31Dec15.tlp'
#graphFile = '../data/test_feedback.tlp'
graph = tlp.loadGraph(graphFile)
percentCompletenessThreshold = 0.0

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
print ffNodeTypes
fbNodeTypes = superTypeDictionary.getTypesFromSuperTypes(['CBb', 'CBa'])

outputCountsStr = 'id, nodeType, isFeedback, isFeedforward, num inputs, num fb outputs, num ff outputs, annotation\n'
inputFromCbStr = 'id, inputs\n'
outputToFfStr = 'id, outputs\n'
outputToFbStr = 'id, outputs\n'

numNeither = 0
numNotSkipped = 0

gcNodesToCBbNodes = {}
ffNodes = tp.utils.getNodesByTypes(ffNodeTypes, graph)
fbNodes = tp.utils.getNodesByTypes(fbNodeTypes, graph)
for node in ffNodes:
    gcNodesToCBbNodes[node] = {}
    for nodeType in fbNodeTypes:
        gcNodesToCBbNodes[node][nodeType] = []

for node in acNodes:

    numNotSkipped += 1
    inputFromCBb = tp.utils.canBeReachedFromTypes(node, fbNodeTypes, graph)
    outputToFb = tp.utils.canReachTypes(node, fbNodeTypes, graph)
    outputToFf = tp.utils.canReachTypes(node, ffNodeTypes, graph)

    isFeedbackNode = (len(inputFromCBb) > 0) and (len(outputToFb) > 0)
    isFeedForwardNode = (len(inputFromCBb) > 0) and (len(outputToFf) > 0)

    id = tp.utils.getNodeId(node, graph)
    nodeType = tp.utils.getNodeType(node, graph)

    if isFeedbackNode or isFeedForwardNode:
        outputCountsStr += id + ', ' + nodeType + ', ' + str(isFeedbackNode) + ', ' + str(isFeedForwardNode) + ', ' + str(len(inputFromCBb)) + ', ' + str(len(outputToFb)) + ', ' + str(len(outputToFf)) + ', ' + str(completeness[node]) + '\n'
    else:
        numNeither += 1


    localPathsStr = ''

    if len(inputFromCBb) > 0:
        for path in inputFromCBb:
            localPathsStr += '[' + path.toStringOfIds() + ']; '
            localPathsStr = localPathsStr.replace(',', '')

        inputFromCbStr += id + ', ' + localPathsStr + '\n'

    localPathsStr = ''

    if len(outputToFf) > 0:
        for path in outputToFf:
            localPathsStr += '[' + path.toStringOfIds() + ']; '
            localPathsStr = localPathsStr.replace(',', '')

        outputToFfStr += id + ', ' + localPathsStr + '\n'

    localPathsStr = ''

    if len(outputToFb) > 0:
        for path in outputToFb:
            localPathsStr += '[' + path.toStringOfIds() + ']; '
            localPathsStr = localPathsStr.replace(',', '')

        outputToFbStr += id + ', ' + localPathsStr + '\n'

    for path in outputToFf:
        gcNode = path.nodes[1]
        print 'gc nodes type is' + tp.utils.getNodeType(gcNode, graph)
        for startPath in inputFromCBb:
            cbbNode = startPath.nodes[0]
            nodeType = tp.utils.getNodeType(cbbNode, graph)
            gcNodesToCBbNodes[gcNode][nodeType].append(cbbNode)

print gcNodesToCBbNodes

stats = open('connectivity_matrix.csv', 'w')
stats.write('nodeid, node label,')
for nodeType in fbNodeTypes:
    stats.write(', ' + nodeType)
stats.write('\n')
for node in gcNodesToCBbNodes.keys():

    check = 0
    for nodeType in fbNodeTypes:
        check += len(gcNodesToCBbNodes[node][nodeType])

    if check == 0:
        print ' skipping node ' + tp.utils.getNodeId(node, graph) + ', ' + tp.utils.getNodeType(node, graph)
        continue


    stats.write(tp.utils.getNodeId(node, graph) + ', ' + tp.utils.getNodeType(node, graph) + ', ')
    for nodeType in fbNodeTypes:
        stats.write(str(len(gcNodesToCBbNodes[node][nodeType])) + ', ')
    stats.write('\n')
stats.close()



stats = open('stats.csv', 'w')
stats.write(outputCountsStr)
stats.close()

stats = open('inputPaths.csv', 'w')
stats.write(inputFromCbStr)
stats.close()

stats = open('outputFf.csv', 'w')
stats.write(outputToFfStr)
stats.close()

stats = open('outputFb.csv', 'w')
stats.write(outputToFbStr)
stats.close()


print 'percent neither ff nor fb: '  + str(numNeither / float(numNotSkipped))

# Render the graph in a node-link diagram.
nodeLinkView = tlpgui.createNodeLinkDiagramView(graph)


