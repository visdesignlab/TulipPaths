from tulip import *
from tulipgui import *
import tulippaths as tp
import json

graphFile = 'shit.tlp'
graph = tlp.loadGraph(graphFile)

def getNodeIndexInDictionary(targetId, nodeDictionaries):
    for i in range(0, len(nodeDictionaries)):
        if nodeDictionaries[i]['name'] == targetId:
            return i
    assert False, "Could not find node"

output = {}
output['nodes'] = []
for node in graph.getNodes():
    nodeAsDict = {}
    nodeAsDict['name'] = tp.utils.getNodeId(node, graph)
    nodeAsDict['group'] = 0
    output['nodes'].append(nodeAsDict)

output['links'] = []
for edge in graph.getEdges():
    source = graph.source(edge)
    target = graph.target(edge)
    sourceIndex = getNodeIndexInDictionary(tp.utils.getNodeId(source, graph), output['nodes'])
    targetIndex = getNodeIndexInDictionary(tp.utils.getNodeId(target, graph), output['nodes'])
    edgeAsDict = {}
    edgeAsDict['source'] = sourceIndex
    edgeAsDict['target'] = targetIndex
    edgeAsDict['value'] = 1
    output['links'].append(edgeAsDict)

print json.dumps(output)