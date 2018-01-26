from FindPathsPlugin import FindPathsPlugin
import tulipplugins


class FindPaths0(FindPathsPlugin):
    """ Tulip plugin algorithm which searches for 1-hop paths """
    def __init__(self, context):
        FindPathsPlugin.__init__(self, context, 0)

# The line below does the magic to register the plugin to the plugin database
# and updates the GUI to make it accessible through the menus.
tulipplugins.registerPlugin("FindPaths0", "Find Nodes (Regex)", "Nathaniel Nelson", "9/3/2016", "", "1.0")
