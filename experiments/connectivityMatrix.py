from tulip import *
from tulipgui import *
import tulippaths as tp
import json

#graphFile = '../data/test_feedback.tlp'
graphFile = '../data/514_10hops.tlp'
graph = tlp.loadGraph(graphFile)

acRegexes = ['AC', 'IAC', 'YAC', 'GAC']
acRegexes = '(?:%s)' % '|'.join(acRegexes)
nodeConstraints = ['CBb.*', acRegexes, 'CBb.*']
edgeConstraints = ['.*', '.*']

"""
matrix = tp.ConnectivityMatrix(graph)
matrix.activate(nodeConstraints, edgeConstraints)
matrix.collapseSources()
matrix.collapseTargets()
jsonObject = matrix.getAsJsonObject(True)
print json.dumps(jsonObject)
"""

nodeConstraints = ['CBb.*', 'CBb.*']
edgeConstraints = ['Gap Junction']
matrix = tp.ConnectivityMatrix(graph)
matrix.activate(nodeConstraints, edgeConstraints)
matrix.collapseSources()
matrix.collapseTargets()
jsonObject = matrix.getAsJsonObject(True)
print json.dumps(jsonObject)