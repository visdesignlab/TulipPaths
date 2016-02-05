from tulip import *
from tulipgui import *
import tulippaths as tp

#graphFile = '../data/test_rodbc_stats.tlp'
graphFile = '../data/514_10hops.tlp'
graph = tlp.loadGraph(graphFile)

superTypeDictionary = tp.SuperTypeDictionary()

# List of all rod bcs
nodeTypes = superTypeDictionary.getTypesFromSuperType('Rod BC')
rodBcNodes = tp.utils.getNodesByTypes(nodeTypes, graph)

# List of all ACs
nodeTypes = superTypeDictionary.getTypesFromSuperTypes(['YAC', 'GAC'])
acNodes = tp.utils.getNodesByTypes(nodeTypes, graph)
print nodeTypes

# List of all CBbs
nodeTypes = superTypeDictionary.getTypesFromSuperTypes(['CBb', 'CBa'])
inputNodes = tp.utils.getNodesByTypes(nodeTypes, graph)
print nodeTypes

rodBcInhibitoryInput = {}
for node in rodBcNodes:
    rodBcInhibitoryInput[node] = []

for node in inputNodes:
    finder = tp.PathFinder(graph)
    finder.findAllPaths(node, 2)
    for path in finder.valid:
        isSynaptic = path.isSynapticPath()
        passesThroughAC = path.nodes[1] in acNodes
        endsOnRodBc = path.nodes[2] in rodBcNodes
        if isSynaptic and passesThroughAC and endsOnRodBc:
            rodBcInhibitoryInput[path.nodes[2]].append(path)

for key in rodBcInhibitoryInput.keys():
    for path in rodBcInhibitoryInput[key]:
        assert path.nodes[2] == key, 'Shit!'

touchedNodes = rodBcNodes
touchedEdges = []
allPaths = []
for key in rodBcInhibitoryInput.keys():
    for path in rodBcInhibitoryInput[key]:
        allPaths.append(path)
        for edge in path.edges:
            touchedEdges.append(edge)
        for node in path.nodes:
            touchedNodes.append(node)

for node in graph.getNodes():
    if node not in touchedNodes:
        graph.delNode(node)

for edge in graph.getEdges():
    if edge not in touchedEdges:
        graph.delEdge(edge)

pathStats = tp.PathStats(allPaths)

uniquePaths = pathStats.getUniqueTypes()
uniqueCount = pathStats.getUniqueTypeCounts()

for i in range (0, len(uniquePaths)):
    print uniquePaths[i].toStringOfTypes() + ' -- ' + str(uniqueCount[i])


dictionary = tp.utils.getDictionaryOfNodeTypes(graph)
for nodeType in dictionary.keys():
    graph.createMetaNode(dictionary[nodeType])

"""
output = 'rodbc id, num inhibitory input paths'
for label in nodeTypes:
    output += ', ' + label
output += '\n'

for node in rodBcNodes:
    output += tp.utils.getNodeId(node, graph) + ', ' + str(len(rodBcInhibitoryInput[node]))
    for label in nodeTypes:
        count = 0
        for path in rodBcInhibitoryInput[node]:
            if tp.utils.getNodeType(path.nodes[0], graph) == label:
                count += 1
        output += ', ' + str(count)
    output += '\n'

print output
"""

tlp.saveGraph(graph, 'test.tlp')
nodeLinkView = tlpgui.createNodeLinkDiagramView(graph)