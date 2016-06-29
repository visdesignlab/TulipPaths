
import tulippaths as tp

class PathFinderWrapper:

    def __init__(self, graph):
        self.graph = graph

    def findRegexConstrainedPaths(self, nodeConstraints, edgeConstraints):

        pathFinder = tp.PathFinder(self.graph)

        pathFinder.findRegexConstrainedPaths(edgeConstraints, nodeConstraints)

        return pathFinder.valid

