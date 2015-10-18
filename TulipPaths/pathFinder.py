""" This object uses a variation of BFS to identify all paths between two nodes in a graph. """

from Queue import *
from config import VERBOSE
from path import *

class PathFinder:

    def __init__(self, graph):
        self.graph = graph
        self.valid = []
        self.failed = []

    def findPaths(self, source, target, maxNumHops):
        assert len(self.valid) == 0 and len(self.failed) == 0, 'Warning - called findPaths before being reset'

        firstPath = Path(self.graph)
        firstPath.addNode(source)

        queue = Queue()
        queue.put(firstPath)

        if VERBOSE:
            print 'starting path search at: ', source
            print 'target node is: ', target

        while not queue.empty():

            currentPath = queue.get()

            if VERBOSE:
                print '  the current path is: ', currentPath.toString()

            if currentPath.size() > maxNumHops:

                if VERBOSE:
                    print '  current path is longer than maxNumHops. adding it to failed paths.'

                self.failed.append(currentPath)

            else:

                currentNode = currentPath.getLastNode()

                if VERBOSE:
                    print '  looking at next nodes from current path'
                    print '  the current node is: ', currentNode

                for nextEdge in self.graph.getOutEdges(currentNode):

                    nextNode = self.graph.target(nextEdge)

                    if VERBOSE:
                        print '    a tentative nextNode is: ', nextNode

                    if currentNode == nextNode:

                        if VERBOSE:
                            print '    currentNode is self connected -- skip this'

                        continue

                    if nextNode == target:

                        nextPath = Path(self.graph, currentPath)
                        nextPath.addNode(nextNode)
                        nextPath.addEdge(nextEdge)

                        if VERBOSE:
                            print '    found the target node: ', nextNode
                            print '    adding succesful path: ', nextPath.toString()

                        self.valid.append(nextPath)

                    else:

                        nextPath = Path(self.graph, currentPath)
                        nextPath.addNode(nextNode)
                        nextPath.addEdge(nextEdge)

                        if VERBOSE:
                            print '    next node is not target node'
                            print '    adding new path: ', nextPath.toString()

                        queue.put(nextPath)

        for path in self.valid:
            assert path.isSane(), "Warning - created bad 'valid' path!'" + path.toString()

        for path in self.failed:
            assert path.isSane(), "Warning - created bad 'failed' path!" + path.toString()

    def reset(self):
        self.valid = []
        self.failed = []
