# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 12:01:59 2014

@author: mohammad
"""

import networkx as nx


# Create a new graph
g = nx.Graph()

# Add some nodes
g.add_node("John")
g.add_node("Maria")
g.add_node("Alex")

# Add some edges beteween nodes
g.add_edge("John", "Alex")
g.add_edge("Maria", "Alex")

# Create a graph
nx.draw(g)
nx.draw_circular(g)
nx.draw_graphviz(g)
nx.draw_random(g)

# Print details of graph
print g.number_of_nodes()
print g.number_of_edges()
print g.nodes()
print g.edges()

# Print degree of specific node and all nodes
print g.degree("John")
print g.degree()




# Create directed graph
di = nx.DiGraph()
di.add_edges_from([("A","B"), ("C","A")])


#draw the graph
nx.draw(di)
nx.draw_circular(di)

# Calculate in and out degrees of all nodes, as maps
print di.in_degree()
print di.out_degree()

# Check neighbours of nodes
print di.neighbors("A")
print di.neighbors("B")
print di.neighbors("C")

print di.successors("A")


# Convert to undirected graph
ug = di.to_undirected()
print ug.neighbors("B")
print ug.neighbors("A")