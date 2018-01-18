# TulipPaths
This is a set of Tulip plugins and python package for analyzing multi-hop relationships in [neuron connectivity graphs](http://connectomes.utah.edu/export/files.html#export-directly-from-a-url).

## Plugins

TulipPaths has plugins for analyzing and cleaning connectome data.

### Find paths plugins

The find paths plugins enable you to search for nodes and path by their labels inside the Tulip GUI.

Input to the 'Find Nodes (Regex)' plugin is a node label regex. This plugin outputs a list of nodes whose labels match the input to regex to your home directory. It also sets Tulip's view selection to the list of nodes. 

Sample input for the 'Find Nodes (Regex)' plugin:

![Find nodes by labels](images/find_nodes.png)

Input to the 'Find n-Hop Paths (Regex)' is similar to the 'Find Nodes (Regex)' plugin. These plugins output a list of paths and update Tulip's view selection.

Sample input for the 'Find 1-Hop Paths (Regex)' plugin:

![Find 1-hop paths](images/find_paths.png)

Sample output from the plugins inside Tulip:

![Output](images/output.png)

### Find Missing Bidirectional Synapses

This plugin will search for bidirectional synapses that are missing reciprocal edges inside tulip.

You can specify which synapse type to search for, the default value is "Gap Junction."

Any edges that the plugin finds are output to the view selection and a user-specified text file. 

## Installation

These instructions assume that you want to use the plugins inside Tulip. If you plan on developing with the plugins, please see the dev environment wiki.

1. Click [this link](https://github.com/visdesignlab/TulipPaths/archive/master.zip) to download TulipPaths-master.zip.
1. Expand TulipPaths-Master.zip into a folder TulipPaths-Master.
1. Prepare the folder to hold the plugins. You may need to create a folder called 'python' in the tulip directory. On MacOS it is /Applications/Tulip-4.8.1.app/Contents/lib/tulip/python. On Windows it is C:\Program Files\Tulip-4.8.1\lib\tulip\python Alternatively, if you have an older version of TulipPaths installed, make sure to delete all files from this directory.
1. Copy the folder TulipPaths-master/tulippaths into the plugins folder.
1. Copy the contents of the folder TulipPaths/plugins into the plugins folder.
1. Check that the plugins folder contains these files:

![Find 1-hop paths](images/installed.png)

You're now ready to run Tulip.
