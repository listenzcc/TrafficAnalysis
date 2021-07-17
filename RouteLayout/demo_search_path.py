'''
FileName: demo_search_path.py
Author: Chuncheng
Version: V0.0
Purpose: The Demo of Search Shortest Path
'''

# %%
from utils.deploy import *
from utils.viz import plot_layout
from utils.graph_methods import compute_dist, mask_dist, spectral_clustering, PathSeacher
from utils.layout_methods import layout_random
from utils.routing_methods import route_least_length, route_between_labels

# %%
nodes = layout_random()

# %%
dist = compute_dist(nodes)
links_shortest = route_least_length(dist)
mdist = mask_dist(dist, links_shortest)
labels = spectral_clustering(mdist)
labels = [str(e) for e in labels]
plot_layout(nodes, color=labels, links=links_shortest, title='Shortest Path')

# %%
ps = PathSeacher()
_dist = mask_dist(dist, links_shortest, mode='mask_unlink', mask_value=np.inf)
m = ps.trace_all(_dist)

# %%
_dist = dist - (m + m.transpose())
links_between = route_between_labels(nodes, _dist, labels)
plot_layout(nodes, color=labels, links=links_between, title='Short Cuts')

# %%
plot_layout(nodes, color=labels, links=links_shortest +
            links_between, title='New Path')

# %%
_dist = mask_dist(dist, links=links_shortest+links_between,
                  mode='mask_unlink', mask_value=np.inf)

ps1 = PathSeacher()
m1 = ps1.trace_all(_dist)

# %%
df_a = pd.DataFrame(m[m != 0], columns=['count'])
df_a['name'] = 'Raw'

df_b = pd.DataFrame(m1[m1 != 0], columns=['count'])
df_b['name'] = 'Between'

df = pd.concat([df_a, df_b], axis=0, ignore_index=True)
df

x = np.sum(m - m1)
px.histogram(df, color='name', opacity=0.5,
             barmode='overlay', title='Gain on Histogram (Gain = {} | {:.2f}%)'.format(x * 2, 100 * x / np.sum(m)))

# %%
mem = ps.memory
mem1 = ps1.memory

# %%
count = np.zeros(len(nodes))
for k, v in tqdm(mem.items()):
    for e in v:
        count[e] += 1

count

count1 = np.zeros(len(nodes))
for k, v in tqdm(mem1.items()):
    for e in v:
        count1[e] += 1

count1

sum(count), sum(count1)

plot_layout(nodes, color=count, links=links_shortest,
            link_color='gray', title='Profits of Nodes (Raw)')

# %%
plot_layout(nodes, color=count1, links=links_shortest +
            links_between, link_color='gray', title='Profits on Nodes (ShortCut)')

# %%
plot_layout(nodes, color=count1-count, links=links_shortest,
            link_color='gray', title='Deficits')

# %%

balance_sheet = dict(
    global_grain=(np.sum(m) - np.sum(m1)) * 2,
    individual_lost=np.sum(count1 - count),
    individual_lost_neg=np.sum((count1 - count)[count1 - count < 0])
)

balance_sheet


# %%
px.bar(sorted(count1 - count), title='Sorted Deficits')

# %%
