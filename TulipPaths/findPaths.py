""" Function for finding paths in a graph """

from Queue import *
from config import VERBOSE
from path import *

def findPaths(startNode, endNode, maxNumHops, graph):
    failedPaths = []
    validPaths = []
    queue = Queue()

    firstPath = Path(graph)
    firstPath.addNode(startNode)
    queue.put(firstPath)

    if VERBOSE:
        print 'starting path search at: ', startNode
        print 'target node is: ', endNode

    while not queue.empty():

        currentPath = queue.get()

        if VERBOSE:
            print '  the current path is: ', currentPath.toString()

        if currentPath.size() > maxNumHops:

            if VERBOSE:
                print '  current path is longer than maxNumHops. adding it to failed paths.'

            failedPaths.append(currentPath)

        else:

            currentNode = currentPath.getLastNode()

            if VERBOSE:
                print '  looking at next nodes from current path'
                print '  the current node is: ', currentNode

            for nextEdge in graph.getOutEdges(currentNode):

                nextNode = graph.target(nextEdge)

                if VERBOSE:
                    print '    a tentative nextNode is: ', nextNode

                if currentNode == nextNode:

                    if VERBOSE:
                        print '    currentNode is self connected -- skip this'

                    continue

                if nextNode == endNode:

                    nextPath = Path(graph, currentPath)
                    nextPath.addNode(nextNode)
                    nextPath.addEdge(nextEdge)

                    if VERBOSE:
                        print '    found the target node: ', nextNode
                        print '    adding succesful path: ', nextPath.toString()

                    validPaths.append(nextPath)

                else:

                    nextPath = Path(graph, currentPath)
                    nextPath.addNode(nextNode)
                    nextPath.addEdge(nextEdge)

                    if VERBOSE:
                        print '    next node is not target node'
                        print '    adding new path: ', nextPath.toString()

                    queue.put(nextPath)

    for path in validPaths:
        assert path.isSane(), "Warning - created bad 'valid' path!'" + path.toString()

    for path in failedPaths:
        assert path.isSane(), "Warning - created bad 'failed' path!" + path.toString()

    return {'validPaths': validPaths,
            'failedPaths': failedPaths}
