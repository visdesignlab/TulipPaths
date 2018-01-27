from FindPathsPlugin import FindPathsPlugin
import tulipplugins


class FindPaths3(FindPathsPlugin):
    """ Tulip plugin algorithm which searches for 3-hop paths """
    def __init__(self, context):
        FindPathsPlugin.__init__(self, context, 3)

# The line below does the magic to register the plugin to the plugin database
# and updates the GUI to make it accessible through the menus.
tulipplugins.registerPlugin("FindPaths3", "Find 3-Hop Paths (Regex)", "Nathaniel Nelson", "9/3/2016", "", "1.0")
