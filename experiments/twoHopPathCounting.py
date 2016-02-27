__author__ = 'Dasha'

from tulip import *
import tulippaths as tp

# Path parameters
graphFile = '../data/514_10hops_22Jan16.tlp'
writeFile = '../data/pathData.json'
sourceNodeId = 485
maxNumHops = 2

# Load the graph
graph = tlp.loadGraph(graphFile)

pathPrinter = tp.PathPrinter(graph)
pathPrinter.printToFile(sourceNodeId, writeFile)

print "Wrote source node ID " + str(sourceNodeId) + "'s data to " + writeFile