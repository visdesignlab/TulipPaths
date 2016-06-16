from tulip import *
import tulippaths as tp

graph = tlp.loadGraph("../data/514_10hops.tlp")

sources = tp.utils.getNodesByTypeRegex("CBb4w", graph)

for source in sources:
    print tp.utils.getNodeType(source, graph)