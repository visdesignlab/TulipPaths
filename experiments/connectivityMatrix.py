from tulip import *
from tulipgui import *
import tulippaths as tp
import json

graphFile = '../data/test_feedback.tlp'
graph = tlp.loadGraph(graphFile)

acRegexes = ['AC', 'IAC', 'YAC', 'GAC', '^Aii']
acRegexes = '(?:%s)' % '|'.join(acRegexes)

nodeConstraints = ['CBb.*', acRegexes, 'GC']
edgeConstraints = ['.*', '.*']



matrix = tp.ConnectivityMatrix(graph)
matrix.activate(nodeConstraints, edgeConstraints)
jsonObject = matrix.getAsJsonObject(False, True)
print json.dumps(jsonObject)