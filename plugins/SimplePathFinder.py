from tulip import *
import tulipplugins
import tulippaths as tp

class SimplePathFinder(tlp.Algorithm):
	def __init__(self, context):
		tlp.Algorithm.__init__(self, context)

		self.sourceLabelName = "source label"
		self.targetIdName = "target id"
		self.numHopsName = "num hops"
		
		self.addStringParameter(self.sourceLabelName, "label where to start", "CBb3m")
		self.addStringParameter(self.sourceLabelName, "label where to start", "CBb3m")
		self.addStringParameter(self.targetIdName, "node id to stop on", "15796")
		self.addIntegerParameter(self.numHopsName, "num hops to search for", "2")

	def check(self):
		return (True, "")

	def run(self):
		viewSelection = self.graph.getBooleanProperty("viewSelection")
		sourceLabel = self.dataSet[self.sourceLabelName]
 		targetId = int(self.dataSet[self.targetIdName])
 		numHops = self.dataSet[self.numHopsName]
		
		# Get all nodes in the starting label
		print 'Setting up source nodes'
		print '    searching for source nodes with label: ' + sourceLabel
		sources = tp.utils.getNodesByType(sourceLabel, self.graph)
		print '    found ' + str(len(sources)) + ' with label ' + sourceLabel
		print ''
		
		# Get the target node
		print 'Searching for target nodes';
		print '    the target node id is ' + str(targetId)
		target = tp.utils.getNodeById(targetId, self.graph)
		print '    found node id ' + str(targetId)
		print ''
		
		# Find paths
	
		print 'Finding paths'
		for source in sources:
			pathFinder = tp.PathFinder(self.graph)
			pathFinder.findPaths(source, target, numHops)
			print '    from node ' + str(tp.utils.getNodeId(source, self.graph)) + ' the paths to ' + str(targetId) + ' are:'
			for path in pathFinder.valid:
				for node in path.nodes:
					viewSelection[node] = True
					
				for edge in path.edges:
					viewSelection[edge] = True
				print '        ' + path.toStringOfTypes()
		
		# Print those paths
		
		return True

# The line below does the magic to register the plugin to the plugin database
# and updates the GUI to make it accessible through the menus.
tulipplugins.registerPlugin("SimplePathFinder", "SimplePathFinder", "", "14/12/2015", "", "1.0")
