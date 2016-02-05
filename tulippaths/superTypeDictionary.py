import json

class SuperTypeDictionary:

    # Parse the json object containing super types.
    def __init__(self):
        self._dictionary = {}

        # This string contains key/value pairs of the different super node types.
        results = json.loads('{ "values": [ { "name": "CBb", "labels": [ "CBb", "CBb3n", "CBb3", "CBb3m", "CBb5w", "CBb4w", "CBb3-4i", "CBb6", "CBb5i", "CBbwf", "CBb [G+]", "CBb5-6", "CBb5-6i", "CBb4i", "CBb5", "CBb6i", "CBb4-5i", "CBb3-4-5i", "CBb4-5-6i", "CBb4iw", "CBb3i", "CBb4", "CBb3-4", "CBbw", "CBbx", "CBb3w [:: CBb3" ] }, { "name": "CBa", "labels": [ "CBa2", "CBa2w", "CBa1", "CBa", "CBab2-3w", "CBab2-4", "CBab2-4w", "CBab2-3", "CBab2-5", "CBabw", "CBa1w", "CBa1-2", "CBa2-3", "CBax" ] }, { "name": "Bipolar cell", "labels": [ "CBx2-3", "CBx", "BCx" ] }, { "name": "YAC", "labels": [ "XAC", "YAC", "YAC Ai", "AC", "YAC ON", "YAC ON/OFF", "YAC OFF", "YAC Starburst", "YAC IAC", "YAC WF", "YAC WF ON/OFF", "AC OFF", "AC Ai", "AC ON", "SAC", "AC extension 91150", "AC 92899 extension", "AC?", "Ac", "AC ON/OFF", "AI-like" ] }, { "name": "Rod BC", "labels": [ "Rod BC" ] }, { "name": "GC", "labels": [ "GC diving", "GC ON", "GC ON/OFF", "GC OFF", "GC Delta L1", "GC direction selective-like", "GC direction selective", "GC fragment", "GC?", "GC" ] }, { "name": "Glia", "labels": [ "MG", "UG" ] }, { "name": "GAC", "labels": [ "GAC", "GAC ON/OFF" ] }, { "name": "GAC Aii", "labels": [ "GAC Aii", "Aii", "Aii", "GAC Aii extension of 223" ] }, { "name": "TH1", "labels": [ "TH1" ] }, { "name": "null", "labels": [ "null" ] } ] }')

        superTypes = results['values']

        for superType in superTypes:

            nodeTypes = []

            for nodeType in superType['labels']:
                nodeTypes.append(str(nodeType))

            superTypeName = str(superType['name'])

            self._dictionary[superTypeName] = nodeTypes

    # Returns the internal dictionary of super types.
    def getDictionary(self):
        return self._dictionary

    # Returns the superType that nodeType belongs to.
    def getSuperTypeFromType(self, nodeType):
        for key in self._dictionary.keys():
            if nodeType in self._dictionary[key]:
                return key
        assert False, 'Could not find super type of nodeType' + nodeType

    # Returns the node types contained in superType
    def getTypesFromSuperType(self, superType):
        if self._dictionary.has_key(superType):
            return self._dictionary[superType]
        else:
            assert False, "Could not find superType == " + superType

    # Returns the node types contained in superTypes
    def getTypesFromSuperTypes(self, superTypes):
        nodeTypes = []

        for superType in superTypes:
            nodeTypes += self.getTypesFromSuperType(superType)

        return nodeTypes

    # Returns true only if nodeType is in superType
    def isTypeInSuperType(self, nodeType, superType):
        return nodeType in self._dictionary[superType]

    # Returns true only if nodeType is in one of the superTypes.
    def isTypeInSuperTypes(self, nodeType, superTypes):
        found = False

        for superType in superTypes:
            found = found or self.isTypeInSuperType(nodeType, superType)

        return found


