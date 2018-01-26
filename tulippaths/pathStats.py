from .path import *
from .pathFinder import *

class PathStats:

    def __init__(self, paths):
        self.paths = paths
        self._loopIndexes = []
        self._uniqueTypeIndexes = []
        self._uniqueTypeCounts = []

        for i in range(0, len(self.paths)):
            path = self.paths[i]

            # Does path contain a loop?
            if path.hasLoop():
                self._loopIndexes.append(i)

            # Is the path a unique type?
            found = False
            for j in range(0, len(self._uniqueTypeIndexes)):
                other = self.paths[self._uniqueTypeIndexes[j]]
                if other.isSameType(path):
                    self._uniqueTypeCounts[j] += 1
                    found = True
                    break

            if not found:
                self._uniqueTypeIndexes.append(i)
                self._uniqueTypeCounts.append(1)

        # Check the unique path counting.
        count = 0
        for i in range(0, len(self._uniqueTypeCounts)):
            count = count + self._uniqueTypeCounts[i]
        assert count == len(self.paths), 'Error - count of unique path types != total num paths'

    def getNumPaths(self):
        return len(self.paths)

    def getNumPathsWithLoop(self):
        return len(self._loopIndexes)

    def getNumUniqueTypes(self):
        return len(self._uniqueTypeIndexes)

    def getUniqueTypes(self):
        unique = []
        for index in self._uniqueTypeIndexes:
            unique.append(self.paths[index])
        return unique

    def getUniqueTypeCounts(self):
        return self._uniqueTypeCounts


