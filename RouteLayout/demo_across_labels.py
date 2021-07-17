'''
FileName: demo_across_labels.py
Author: Chuncheng
Version: V0.0
Purpose: The Demo of Plotting Graph with Connections across Labels
'''

# %%
import numpy as np
from utils.viz import plot_layout
from utils.graph_methods import compute_dist, mask_dist, spectral_clustering
from utils.layout_methods import layout_random
from utils.routing_methods import route_least_length, route_between_labels

# %%
nodes = layout_random()

# %%
dist = compute_dist(nodes)
links = route_least_length(dist)
mdist = mask_dist(dist, links)
labels = spectral_clustering(mdist)
plot_layout(nodes, color=labels)

# %%
a_links = route_between_labels(nodes, dist, labels)
a_links

# %%
plot_layout(nodes, color=labels, links=links)

# %%
plot_layout(nodes, color=labels, links=a_links)

# %%
plot_layout(nodes, color=labels, links=links + a_links)

# %%
