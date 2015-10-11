""" Function for finding paths in a graph """

from Queue import *
from tulip import *
from config import VERBOSE

def findPaths(startNode, endNode, maxNumHops, graph):

    failedPaths = []
    validPaths = []
    queue = Queue()
    queue.put([startNode])

    if VERBOSE:
        print 'starting path search at: ', startNode
        print 'target node is: ', endNode

    while not queue.empty():

        currentPath = queue.get()

        if VERBOSE:
            print '  the current path is: ', currentPath

        if len(currentPath) > maxNumHops:

            if VERBOSE:
                print '  current path is longer than maxNumHops. adding it to failed paths.'

            failedPaths.append(currentPath)

        else:

            currentNode = currentPath[len(currentPath) - 1]

            if VERBOSE:
                print '  looking at next nodes from current path'
                print '  the current node is: ', currentNode

            for nextNode in graph.getOutNodes(currentNode):

                if VERBOSE:
                    print '    a tentative nextNode is: ', nextNode

                if currentNode == nextNode:

                    if VERBOSE:
                        print '    currentNode is self connected -- skip this'

                    continue

                if nextNode == endNode:

                    nextPath = list(currentPath)
                    nextPath.append(nextNode)

                    if VERBOSE:
                        print '    found the target node: ', nextNode
                        print '    adding succesful path: ', nextPath

                    validPaths.append(nextPath)

                else:
                    nextPath = list(currentPath)
                    nextPath.append(nextNode)

                    if VERBOSE:
                        print '    next node is not target node'
                        print '    adding new path: ', nextPath

                    queue.put(nextPath)

    print 'the failed paths are ', failedPaths
    print 'the valid paths are ', validPaths
    return validPaths