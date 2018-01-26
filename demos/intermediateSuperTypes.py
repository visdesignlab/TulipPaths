""" Example using the SuperTypeDictionary object.
 This finds a list of all nodes in the super types YAC and GAC.
 It then computes the percent completeness for all
 of these nodes.
"""

from tulip import *
from tulipgui import *
import tulippaths as tp

graphFile = '../data/514_4hops.tlp'
graph = tlp.loadGraph(graphFile)

completeness = tp.utils.getApproximateAnnotationCompleteness(graph)

superTypeDictionary = tp.SuperTypeDictionary()

nodeTypes = superTypeDictionary.getTypesFromSuperTypes(['YAC', 'GAC'])

nodes = tp.utils.getNodesByTypes(nodeTypes, graph)

for node in nodes:
    print((str(tp.utils.getNodeId(node, graph)) + ', ' + str(completeness[node])))