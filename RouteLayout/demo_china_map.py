'''
FileName: demo_china_map.py
Author: Chuncheng
Version: V0.0
Purpose: Demo of Routing of China Map
'''

# %%
from utils.layout_nodes import layout_chinese_cities, layout_random
from utils.route_nodes import route_least_length, plot_routing

# %%
nodes = layout_chinese_cities()
nodes = layout_random()

route, dist = route_least_length(nodes)

fig = plot_routing(nodes, route)

# %%
