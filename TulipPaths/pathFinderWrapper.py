
import tulippaths as tp

class PathFinderWrapper:

    def __init__(self, graph):
        self.graph = graph

    def findConstrainedPathsFromType(self, sourceType, nodeConstraints, edgeConstraints):

        sources = tp.utils.getNodesByType(sourceType, self.graph)

        paths = []

        for source in sources:
            paths += self.findConstrainedPathsFromSource(source, nodeConstraints, edgeConstraints)

        return paths

    def findConstrainedPathsFromSource(self, source, nodeConstraints, edgeConstraints):

        pathFinder = tp.PathFinder(self.graph)

        pathFinder.findConstrainedPaths(source, nodeConstraints, edgeConstraints)

        return pathFinder.valid



