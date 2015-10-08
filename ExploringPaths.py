from tulip import *
import tulipplugins

class ExploringPaths(tlp.Algorithm):
	def __init__(self, context):
		tlp.Algorithm.__init__(self, context)
		# you can add parameters to the plugin here through the following syntax
		# self.add<Type>Parameter("<paramName>", "<paramDoc>", "<paramDefaultValue>")
		# (see documentation of class tlp.WithParameter to see what types of parameters are supported)

	def check(self):
		# This method is called before applying the algorithm on the input graph.
		# You can perform some precondition checks here.
		# See comments in the run method to know how to access to the input graph.

		# Must return a tuple (boolean, string). First member indicates if the algorithm can be applied
		# and the second one can be used to provide an error message
		return (True, "")

	def run(self):

		### Function definitions
		
		# Returns a node of the desired id or -1 if no node is found.
		# I'm passing in nodeIds and graph here to make the input explicit.
		def getNodeByID(id, nodeIds, graph):
			for node in graph.getNodes():
					if int(nodeIds[node]) == id:
						return node
			return -1

		# TODO: fill this in. This is where your BFS will come in handy.
		def findPaths(startNode, endNode, maxNumHops, nodeIds, graph):
			paths = []
			return paths

		### Actually do the work here. 
		
		# Initialize array of node properties.
		nodeIds = self.graph.getProperty("ID")
		
		startNode = getNodeByID(176, nodeIds, self.graph)
		endNode = getNodeByID(606, nodeIds, self.graph)
		
		# Sanity check that we found the nodes.
		print 'Start node is: ' + str(startNode)
		print 'End node is: ' + str(endNode)

		# TODO: think about the expected input and output for these simple cases first. Things to think about:
		# -what do you expect the output to be? 
		# -how will you handle cycles? 
		# -how will you exit early when paths are longer than maxNumHops?
		maxNumHops = 1
		paths = findPaths(startNode, endNode, maxNumHops, nodeIds, self.graph)
		print 'Found paths are: ' + str(paths)

		return True

# The line below does the magic to register the plugin to the plugin database
# and updates the GUI to make it accessible through the menus.
tulipplugins.registerPlugin("ExploringPaths", "ExploringPaths", "", "08/10/2015", "", "1.0")
