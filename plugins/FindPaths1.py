from FindPathsPlugin import FindPathsPlugin
import tulipplugins


class FindPaths1(FindPathsPlugin):
    """ Tulip plugin algorithm which searches for 1-hop paths """
    def __init__(self, context):
        FindPathsPlugin.__init__(self, context, 1)

# The line below does the magic to register the plugin to the plugin database
# and updates the GUI to make it accessible through the menus.
tulipplugins.registerPlugin("FindPaths1", "Find 1-Hop Paths (Regex)", "Nathaniel Nelson", "14/12/2015", "", "1.0")
