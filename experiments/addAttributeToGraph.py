from tulip import *
from tulipgui import *
import tulippaths as tp


def addAttributeToGraph(graph, attribute, filename):

    def parseCsv(filename):
        file = open(filename)
        dictionary = {}
        for line in file:
            line = line.split(',')
            dictionary[int(line[0])] = float(line[1])
        return dictionary

    attributeDictionary = parseCsv(filename)
    attributeProperty = graph.getDoubleProperty(attribute)

    for node in graph.getNodes():
        id = tp.utils.getNodeId(node, graph)
        if int(id) in attributeDictionary.keys():
            attributeProperty[node] = attributeDictionary[int(id)]
        else:
            attributeProperty[node] = 100

    return graph


graph = tlp.loadGraph('../data/test_feedback.tlp')
graph = addAttributeToGraph(graph, 'locations', '../data/num_location_annotations.csv')
graph = addAttributeToGraph(graph, 'hull area', '../data/convex_hull_area.csv')
tlp.saveGraph(graph, 'test_feedback.tlp')