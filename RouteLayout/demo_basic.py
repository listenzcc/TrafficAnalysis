'''
FileName: demo_basic.py
Author: Chuncheng
Version: V0.0
Purpose: The 1st Demo of Layout Nodes and Plot them
'''

# %%
from utils.layout_nodes import layout_random, layout_chinese_cities, plot_layout

# %%
nodes1 = layout_random()

# %%
nodes2 = layout_chinese_cities()

# %%
fig1 = plot_layout(nodes1)

# %%
fig2 = plot_layout(nodes2)

# %%
