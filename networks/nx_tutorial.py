#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 17:21:16 2020

@author: ShaunGan
"""
#%%

import networkx as nx

G = nx.Graph()

#G.add_node(1)
#H = nx.path_graph(10)
#G.add_nodes_from(H)
G.add_nodes_from([1,2,3])

G.add_edge(1,2)
#G.add_edges_from([(2,1),(1,3)])

nx.draw(G, with_labels=True, font_weight='bold')

G.clear()
nx.draw(G, with_labels=True, font_weight='bold')