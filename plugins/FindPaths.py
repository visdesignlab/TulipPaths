from tulip import *
import tulipplugins
import tulippaths as tp

class FindPaths(tlp.Algorithm):
	def __init__(self, context):
		tlp.Algorithm.__init__(self, context)

		self.nodeLabel0 = "node #0 label"
		self.nodeLabel1 = "node #1 label"
		self.nodeLabel2 = "node #2 label"
		
		self.edgeType0 = "edge #0 type"
		self.edgeType1 = "edge #1 type"

		self.addStringParameter(self.nodeLabel0, "", "CBb3m")
		self.addStringParameter(self.edgeType0, "", "Ribbon Synapse")
		self.addStringParameter(self.nodeLabel1, "", "AC")
		self.addStringParameter(self.edgeType1, "", "Conventional")
		self.addStringParameter(self.nodeLabel2, "", "Rod BC")

	def check(self):
		return (True, "")

	def run(self):
		
		sourceLabel = self.dataSet[self.nodeLabel0]
		targetLabel = self.dataSet[self.nodeLabel2]
		middleLabel = self.dataSet[self.nodeLabel1]
		# Get all nodes in the starting label
		print 'Setting up source nodes'
		print '    searching for source nodes with label: ' + sourceLabel
		sources = tp.utils.getNodesByType(sourceLabel, self.graph)
		print '    found ' + str(len(sources)) + ' nodes with label ' + sourceLabel
		print ''
		
		# Get the target node
		print 'Searching for target nodes';
		print '    the target node label is ' + targetLabel
		targets = tp.utils.getNodesByType(targetLabel, self.graph)
		print '    found ' + str(len(targets)) + ' nodes with label ' + targetLabel
		print ''
		
		# Find paths
	
		print 'Finding paths'
		for source in sources:
			for target in targets:
				pathFinder = tp.PathFinder(self.graph)
				pathFinder.findPaths(source, target, 3)
				for path in pathFinder.valid:
					if tp.utils.getNodeType(path.nodes[1], self.graph) == middleLabel:
						print '    from node ' + str(tp.utils.getNodeId(source, self.graph)) + ' the paths to ' + str(tp.utils.getNodeId(target, self.graph)) + ' are:'	
						print '        ' + path.toStringOfTypes()
		
		# Print those paths
		return True

# The line below does the magic to register the plugin to the plugin database
# and updates the GUI to make it accessible through the menus.
tulipplugins.registerPlugin("FindPaths", "FindPaths", "", "14/12/2015", "", "1.0")
