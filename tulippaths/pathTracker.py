class PathTracker:

    def __init__(self):
        self._paths = []

    def getOrCreatePathTypeID(self, path):
        for i in range(0, len(self._paths)):
            if self._paths[i].isSameType(path):
                return i

        self._paths.append(path)

        return len(self._paths) - 1

    def getNumUniquePathTypes(self):
        return len(self._paths)