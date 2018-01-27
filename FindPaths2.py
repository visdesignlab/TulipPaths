from FindPathsPlugin import FindPathsPlugin
import tulipplugins


class FindPaths2(FindPathsPlugin):
    """ Tulip plugin algorithm which searches for 2-hop paths """
    def __init__(self, context):
        FindPathsPlugin.__init__(self, context, 2)

# The line below does the magic to register the plugin to the plugin database
# and updates the GUI to make it accessible through the menus.
tulipplugins.registerPlugin("FindPaths2", "Find 2-Hop Paths (Regex)", "Nathaniel Nelson", "9/3/2016", "", "1.0")
