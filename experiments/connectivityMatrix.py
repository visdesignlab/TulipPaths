from tulip import *
from tulipgui import *
import tulippaths as tp
import json

#graphFile = '../data/test_feedback.tlp'
graphFile = '../data/514_10hops_22Jan16.tlp'
graph = tlp.loadGraph(graphFile)

acRegexes = ['AC', 'IAC', 'YAC', 'GAC', '^Aii']
acRegexes = '(?:%s)' % '|'.join(acRegexes)

#nodeConstraints = ['CBb5$', acRegexes, 'CBb5$']
#edgeConstraints = ['Ribbon Synapse', 'Conventional']
#print nodeConstraints
#print edgeConstraints


#matrix = tp.ConnectivityMatrix(graph)
#matrix.activate(nodeConstraints, edgeConstraints)
#matrix.collapseSources()
#matrix.collapseTargets()
#jsonObject = matrix.getAsJsonObject(False)
#print json.dumps(jsonObject)

"""
nodeConstraints = ['CBb.*', 'CBb.*']
edgeConstraints = ['Gap Junction']
matrix = tp.ConnectivityMatrix(graph)
matrix.activate(nodeConstraints, edgeConstraints)
matrix.collapseSources()
matrix.collapseTargets()
jsonObject = matrix.getAsJsonObject(True)
print json.dumps(jsonObject)
"""

nodeConstraints = [acRegexes, 'CBb5$']
edgeConstraints = ['.*']
completeness = tp.utils.getApproximateAnnotationCompleteness(graph)

acs = tp.utils.getNodesByTypeRegex(nodeConstraints[0], graph)
for node in acs:
    if completeness[node] < .2:
        graph.delNode(node)

print 'creating matrix'
matrix = tp.ConnectivityMatrix(graph)
print 'activate matrix'
matrix.activate(nodeConstraints, edgeConstraints)
print 'collapse sources'
#matrix.collapseSources()
#matrix.collapseTargets()
jsonObject = matrix.getAsJsonObject(True)
print json.dumps(jsonObject)