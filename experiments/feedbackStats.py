from tulip import *
from tulipgui import *
import tulippaths as tp
import json
graphFile = '../data/514_10hops_22Jan16.tlp'
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
numAcsInMotif = {}
ffNodes = tp.utils.getNodesByTypes(ffNodeTypes, graph)
fbNodes = tp.utils.getNodesByTypes(fbNodeTypes, graph)
for node in ffNodes:
    gcNodesToCBbNodes[node] = {}
    numAcsInMotif[node] = {}
    for nodeType in fbNodeTypes:
        gcNodesToCBbNodes[node][nodeType] = []
        numAcsInMotif[node][nodeType] = []

markedNodes = []
markedEdges = []

for node in acNodes:

    numNotSkipped += 1
    inputFromCBb = tp.utils.canBeReachedFromTypes(node, fbNodeTypes, graph)
    outputToFb = tp.utils.canReachTypes(node, fbNodeTypes, graph)
    outputToFf = tp.utils.canReachTypes(node, ffNodeTypes, graph)

    isFeedbackNode = (len(inputFromCBb) > 0) and (len(outputToFb) > 0)
    isFeedForwardNode = (len(inputFromCBb) > 0) and (len(outputToFf) > 0)

    if isFeedbackNode or isFeedForwardNode:
        for results in [outputToFb, outputToFf, inputFromCBb]:
            for path in results:
                for temp in path.nodes:
                    if temp not in markedNodes:
                        markedNodes.append(temp)
                for temp in path.edges:
                    if temp not in markedEdges:
                        markedEdges.append(temp)

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
            if node not in numAcsInMotif[gcNode][nodeType]:
                numAcsInMotif[gcNode][nodeType].append(node)
            gcNodesToCBbNodes[gcNode][nodeType].append(cbbNode)


print gcNodesToCBbNodes

ids = [606 ,6857 ,15796 ,5107 ,8575 ,74047 ,53399 ,53436 ,54695 ,54701 ,52882 ,8580 ,70924 ,64887 ,64923 ,7594 ,31024 ,29198 ,68539 ,16087, 5118]
#desiredLabels = ["CBb3m", "CBb5w", "CBb4w", "CBb3-4i", "CBb5i", "CBb5-6i", "CBb4i", "CBb3-4-5i", "CBb3", "CBb4-5-6i", "CBb3i"]
desiredLabels = superTypeDictionary.getTypesFromSuperTypes(['CBb', 'CBa'])
stats = open('connectivity_matrix_counting_motifs.csv', 'w')
stats.write('node id, node label')
for nodeType in desiredLabels:
    stats.write(', ' + nodeType)
stats.write('\n')

for id in ids:
    node = tp.utils.getNodeById(id, graph)
    check = 0
    for nodeType in desiredLabels:
        check += len(numAcsInMotif[node][nodeType])

    if check == 0:
        print ' skipping node ' + tp.utils.getNodeId(node, graph) + ', ' + tp.utils.getNodeType(node, graph)
        continue
    stats.write(tp.utils.getNodeId(node, graph) + ', ' + tp.utils.getNodeType(node, graph) + ', ')
    for nodeType in desiredLabels:
        stats.write(str(len(numAcsInMotif[node][nodeType])) + ', ')
    stats.write('\n')
stats.close()

stats = open('connectivity_matrix.csv', 'w')
stats.write('nodeid, node label')
for nodeType in desiredLabels:
    if len(tp.utils.getNodesByType(nodeType, graph)) > 0:
        stats.write(', ' + nodeType)
stats.write('\n')
for id in ids:
    node = tp.utils.getNodeById(id, graph)
    for nodeType in desiredLabels:
        check += len(gcNodesToCBbNodes[node][nodeType])

    if check == 0:
        print ' skipping node ' + tp.utils.getNodeId(node, graph) + ', ' + tp.utils.getNodeType(node, graph)
        continue

    stats.write(tp.utils.getNodeId(node, graph) + ', ' + tp.utils.getNodeType(node, graph) + ', ')
    for nodeType in desiredLabels:
            if len(tp.utils.getNodesByType(nodeType, graph)) > 0:
                stats.write(str(len(gcNodesToCBbNodes[node][nodeType])) + ', ')
    stats.write('\n')
stats.close()

stats = open('connectivity_matrix_count_unique_cbbs.csv', 'w')
stats.write('nodeid, node label')
for nodeType in desiredLabels:
    stats.write(', ' + nodeType)
stats.write('\n')

for id in ids:
    node = tp.utils.getNodeById(id, graph)
    check = 0
    for nodeType in desiredLabels:
        check += len(gcNodesToCBbNodes[node][nodeType])

    if check == 0:
        print ' skipping node ' + tp.utils.getNodeId(node, graph) + ', ' + tp.utils.getNodeType(node, graph)
        continue

    stats.write(tp.utils.getNodeId(node, graph) + ', ' + tp.utils.getNodeType(node, graph) + ', ')
    for nodeType in desiredLabels:
        nodeSet = set(gcNodesToCBbNodes[node][nodeType])
        stats.write(str(len(nodeSet)) + ', ')
    stats.write('\n')
stats.close()

acUsage = {}

for id in ids:
    node = tp.utils.getNodeById(id, graph)
    for nodeType in desiredLabels:
        acs = numAcsInMotif[node][nodeType]
        for ac in acs:
            if acUsage.has_key(ac):
                acUsage[ac].append(id)
            else:
                acUsage[ac] = [id]

stats = open('ac_usage.csv', 'w')
stats.write('ac id, ac label, num usage, usage string\n')
for key in acUsage.keys():
    id = tp.utils.getNodeId(key, graph)
    type = tp.utils.getNodeType(key, graph)
    listOfGcs = ''
    for gc in acUsage[key]:
        listOfGcs += str(gc) + ';'

    stats.write(str(id) + ', ' +  type + ', ' + str(len(acUsage[key])) + ', ' + listOfGcs + '\n')
stats.close()

# for each ac being used
stats = open('acs_connectivity_matrix.csv', 'w')
stats.write('node, label')
for label in desiredLabels:
    stats.write(',' + label)
stats.write('\n')
for acNode in acUsage.keys():
    stats.write(str(tp.utils.getNodeId(acNode, graph)))
    stats.write(', ' + str(tp.utils.getNodeType(acNode, graph)) + ',' )
    for label in desiredLabels:
        # count the number of times it is used
        usage = []
        for id in ids:
            gc = tp.utils.getNodeById(id, graph)
            listOfGcsAcs = numAcsInMotif[gc][label]
            for temp in listOfGcsAcs:
                if temp == acNode:
                  usage.append(gc)
        stats.write(str(len(usage))+',')
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

for node in graph.getNodes():
    if node not in markedNodes:
        graph.delNode(node)

for edge in graph.getEdges():
    if edge not in markedEdges:
        graph.delEdge(edge)

tlp.saveGraph(graph, 'shit.tlp')
nodeLinkView = tlpgui.createNodeLinkDiagramView(graph)


