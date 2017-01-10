# import networkx as nx
# import matplotlib.pyplot as plt
#
# G=nx.random_geometric_graph(200,0.125)
# # position is stored as node attribute data for random_geometric_graph
# pos=nx.get_node_attributes(G,'pos')
#
# # find node near center (0.5,0.5)
# dmin=1
# ncenter=0
# for n in pos:
#     x,y=pos[n]
#     d=(x-0.5)**2+(y-0.5)**2
#     if d<dmin:
#         ncenter=n
#         dmin=d
#
# # color by path length from node near center
# p=nx.single_source_shortest_path_length(G,ncenter)
#
# plt.figure(figsize=(8,8))
# nx.draw_networkx_edges(G,pos,nodelist=[ncenter],alpha=0.4)
# nx.draw_networkx_nodes(G,pos,nodelist=p.keys(),
#                        node_size=80,
#                        node_color=p.values(),
#                        cmap=plt.cm.Reds_r)
#
# plt.xlim(-0.05,1.05)
# plt.ylim(-0.05,1.05)
# plt.axis('off')
# plt.savefig('random_geometric_graph.png')
# plt.show()

# #!/usr/bin/env python
# """
# Random graph from given degree sequence.
# Draw degree rank plot and graph with matplotlib.
# """
# __author__ = """Aric Hagberg <aric.hagberg@gmail.com>"""
# import networkx as nx
# import matplotlib.pyplot as plt
# G = nx.gnp_random_graph(100,0.02)
#
# degree_sequence=sorted(nx.degree(G).values(),reverse=True) # degree sequence
# #print "Degree sequence", degree_sequence
# dmax=max(degree_sequence)
#
# plt.loglog(degree_sequence,'b-',marker='o')
# plt.title("Degree rank plot")
# plt.ylabel("degree")
# plt.xlabel("rank")
#
# # draw graph in inset
# plt.axes([0.45,0.45,0.45,0.45])
# Gcc=sorted(nx.connected_component_subgraphs(G), key = len, reverse=True)[0]
# pos=nx.spring_layout(Gcc)
# plt.axis('off')
# nx.draw_networkx_nodes(Gcc,pos,node_size=20)
# nx.draw_networkx_edges(Gcc,pos,alpha=0.4)
#
# plt.savefig("degree_histogram.png")
# plt.show()

# #!/usr/bin/env python
# """
# Routes to LANL from 186 sites on the Internet.
#
# This uses Graphviz for layout so you need PyGraphviz or Pydot.
#
# """
# __author__ = """Aric Hagberg (hagberg@lanl.gov)"""
# #    Copyright (C) 2004-2015
# #    Aric Hagberg <hagberg@lanl.gov>
# #    Dan Schult <dschult@colgate.edu>
# #    Pieter Swart <swart@lanl.gov>
# #    All rights reserved.
# #    BSD license.
#
#
# def lanl_graph():
#     """ Return the lanl internet view graph from lanl.edges
#     """
#     import networkx as nx
#     try:
#         fh=open('lanl_routes.edgelist','r')
#     except IOError:
#         print("lanl.edges not found")
#         raise
#
#     G=nx.Graph()
#
#     time={}
#     time[0]=0 # assign 0 to center node
#     for line in fh.readlines():
#         (head,tail,rtt)=line.split()
#         G.add_edge(int(head),int(tail))
#         time[int(head)]=float(rtt)
#
#     # get largest component and assign ping times to G0time dictionary
#     G0=sorted(nx.connected_component_subgraphs(G), key = len, reverse=True)[0]
#     G0.rtt={}
#     for n in G0:
#         G0.rtt[n]=time[n]
#
#     return G0
#
# if __name__ == '__main__':
#
#     import networkx as nx
#     import math
#     try:
#         from networkx import graphviz_layout
#     except ImportError:
#         raise ImportError("This example needs Graphviz and either PyGraphviz or Pydot")
#
#     G=lanl_graph()
#
#     print("graph has %d nodes with %d edges"\
#           %(nx.number_of_nodes(G),nx.number_of_edges(G)))
#     print(nx.number_connected_components(G),"connected components")
#
#     import matplotlib.pyplot as plt
#     plt.figure(figsize=(8,8))
#     # use graphviz to find radial layout
#     pos=nx.graphviz_layout(G,prog="twopi",root=0)
#     # draw nodes, coloring by rtt ping time
#     nx.draw(G,pos,
#             node_color=[G.rtt[v] for v in G],
#             with_labels=False,
#             alpha=0.5,
#             node_size=15)
#     # adjust the plot limits
#     xmax=1.02*max(xx for xx,yy in pos.values())
#     ymax=1.02*max(yy for xx,yy in pos.values())
#     plt.xlim(0,xmax)
#     plt.ylim(0,ymax)
#     plt.savefig("lanl_routes.png")

#!/usr/bin/env python
"""
Compute some network properties for the lollipop graph.
"""
#    Copyright (C) 2004-2016 by
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    All rights reserved.
#    BSD license.

from networkx import *
import matplotlib.pyplot as plt

G = lollipop_graph(4,6)

pathlengths=[]

print("source vertex {target:length, }")
for v in G.nodes():
    spl=single_source_shortest_path_length(G,v)
    print('%s %s' % (v,spl))
    for p in spl.values():
        pathlengths.append(p)

print('')
print("average shortest path length %s" % (sum(pathlengths)/len(pathlengths)))

# histogram of path lengths
dist={}
for p in pathlengths:
    if p in dist:
        dist[p]+=1
    else:
        dist[p]=1

print('')
print("length #paths")
verts=dist.keys()
for d in sorted(verts):
    print('%s %d' % (d,dist[d]))

print("radius: %d" % radius(G))
print("diameter: %d" % diameter(G))
print("eccentricity: %s" % eccentricity(G))
print("center: %s" % center(G))
print("periphery: %s" % periphery(G))
print("density: %s" % density(G))

nx.draw(G)
plt.show()