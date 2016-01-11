
import tulippaths as tp

class PathFinderWrapper:

    def __init__(self, graph):
        self.graph = graph

    def findConstrainedPathsFromType(self, sourceType, edgeConstraints, nodeConstraints):

        sources = tp.utils.getNodesByType(sourceType, self.graph)

        paths = []

        for source in sources:
            paths += self.findConstrainedPathsFromSource(source, edgeConstraints, nodeConstraints)

        return paths

    def findConstrainedPathsFromSource(self, source, edgeConstraints, nodeConstraints):

        pathFinder = tp.PathFinder(self.graph)

        pathFinder.findConstrainedPaths(source, edgeConstraints, nodeConstraints)

        return pathFinder.valid



