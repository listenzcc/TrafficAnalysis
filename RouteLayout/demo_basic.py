'''
FileName: demo_basic.py
Author: Chuncheng
Version: V0.0
Purpose: The Demo of Basic Graph Plotting
'''

# %%
from utils.viz import plot_layout
from utils.graph_methods import compute_dist, mask_dist, spectral_clustering
from utils.layout_methods import layout_random
from utils.routing_methods import route_least_length

# %%
nodes = layout_random()

# %%
dist = compute_dist(nodes)
links = route_least_length(dist)
mdist = mask_dist(dist, links)
labels = spectral_clustering(mdist)
plot_layout(nodes, color=labels)

# %%
plot_layout(nodes, color=labels, links=links)

# %%
