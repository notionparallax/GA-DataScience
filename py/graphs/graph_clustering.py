# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 12:01:59 2014

@author: mohammad
"""

import networkx as nx
import numpy as np
import matplotlib as plt
import json
from scipy.cluster import hierarchy
from scipy.spatial import distance

# Load standard "Karate club" graph
g = nx.read_edgelist("karate.edgelist")
print "%d nodes, %d edges" % ( len(g.nodes()), len(g.edges()) )

nx.draw_graphviz(g)
nx.draw_networkx(g)


# Build a distance matrix, based on shortest paths
path_length = nx.all_pairs_shortest_path_length(g)

path_length.viewkeys()
print path_length['24']


n = len(g.nodes())
distances=np.zeros((n,n))


for u,p in path_length.iteritems():
    for v, d in p.iteritems():
        print json.dumps([u ,p ,v ,d], indent=3)
    
    
for u,p in path_length.iteritems():
	for v,d in p.iteritems():
		distances[int(u)-1][int(v)-1] = d
		

# Apply average-linkage agglomerative clustering
Y = distance.squareform(distances)
Z = hierarchy.average(distances)
ZY = hierarchy.average(Y)

# Generate the tree and save it to disk
hierarchy.dendrogram(Z)
hierarchy.dendrogram(ZY)

plt.pylab.savefig("tree.png", format="png")
