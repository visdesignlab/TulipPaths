from tulip import *
from tulipgui import *
import tulippaths as tp
import json

graphFile = '../data/test_feedback.tlp'
#graphFile = '../data/514_10hops.tlp'
graph = tlp.loadGraph(graphFile)

acRegexes = ['AC', 'IAC', 'YAC']
acRegexes = '(?:%s)' % '|'.join(acRegexes)
nodeConstraints = ['CBb.*', acRegexes, 'GC']
edgeConstraints = ['.*', '.*']

matrix = tp.ConnectivityMatrix(graph)
matrix.activate(nodeConstraints, edgeConstraints)
jsonObject = matrix.getPathCountJsonMatrix()
print json.dumps(jsonObject)

