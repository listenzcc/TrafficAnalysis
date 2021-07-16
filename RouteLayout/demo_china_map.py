'''
FileName: demo_china_map.py
Author: Chuncheng
Version: V0.0
Purpose: Demo of Routing of China Map
'''

# %%
from utils.viz import plot_layout
from utils.graph_methods import compute_dist, mask_dist, spectral_clustering
from utils.layout_methods import layout_random, layout_chinese_cities
from utils.routing_methods import route_least_length

# %%
nodes = layout_chinese_cities()

# %%
dist = compute_dist(nodes)
links = route_least_length(nodes, dist)
mdist = mask_dist(dist, links)
labels = spectral_clustering(mdist)
plot_layout(nodes, color=[str(e) for e in labels])

# %%
plot_layout(nodes, color=[str(e) for e in labels], links=links)

# %%
