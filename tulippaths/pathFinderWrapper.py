
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

    def findConstrainedPathsFromTypeRegex(self, sourceTypeRegex, nodeConstraints, edgeConstraints):

        sources = tp.utils.getNodesByTypeRegex(sourceTypeRegex, self.graph)

        paths = []

        for source in sources:
            paths += self.findRegexConstrainedPathsFromSource(source, nodeConstraints, edgeConstraints)

        return paths

    def findConstrainedPathsFromSource(self, source, nodeConstraints, edgeConstraints):

        pathFinder = tp.PathFinder(self.graph)

        pathFinder.findConstrainedPaths(source, nodeConstraints, edgeConstraints)

        return pathFinder.valid

    def findRegexConstrainedPathsFromSource(self, source, nodeConstraints, edgeConstraints):

        pathFinder = tp.PathFinder(self.graph)

        pathFinder.findRegexConstrainedPaths(source, nodeConstraints, edgeConstraints)

        return pathFinder.valid

