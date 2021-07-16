'''
FileName: least_length.py
Author: Chuncheng
Version: V0.11
Purpose: Layout Route by Least Length Law
         Special Version of China Map
'''

# %%
import json
import geopandas as gpd
from sklearn.cluster import SpectralClustering
from settings import *

# %%
GeoDataFolder

# %%


def read_geojson(adcode):
    '''
    Method: read_geojson

    Read GeoJson of [adcode],
    and Generate Features.

    Args:
    - @adcode

    Outputs:
    - The features

    '''
    path = os.path.join(GeoDataFolder, '{}_full.json'.format(adcode))
    try:
        geojson = json.load(open(path))
    except FileNotFoundError:
        return None
    print('D: Fetched GeoJson from {}'.format(path))

    features = gpd.GeoDataFrame.from_features(geojson['features'])
    features = pd.DataFrame(features)
    # Overwrite the Geometry to Prevent Too Large
    features['geometry'] = '--'
    print('D: Parsed Features from {}'.format(adcode))

    features = features.query('adcode != "{}"'.format(adcode))
    return features


# %%
df = read_geojson(100000)

dfs = []
for code in tqdm(df['adcode'].values):
    dfs.append(read_geojson(code))

df_all = pd.concat(dfs, axis=0)
df_all.index = range(len(df_all))
df_all['parent'] = df_all['parent'].map(lambda e: e['adcode'])
df_all

# %%

d = np.array([e for e in df_all['center'].values if isinstance(e, list)])
nodes = pd.DataFrame(d, columns=['x', 'y'])
nodes

# %%
# nodes = pd.read_json(os.path.join(MiddleFolder, 'nodes.json'))
# nodes

# %%


@ timer
def mk_route_least_length(df, dist=None, start=0, end=-1):
    '''
    Method: mk_route_least_length

    Make Routing Link to the graph of [df],
    - The start idx is [start];
    - The end idx is [end];
    - The end is -1 refers Routing all the Nodes;
    - The dist refers the distance between Nodes,
      if the dist is not given, the matrix is calculated based on Norm2.

    Todo:
    - How to use Customized [dist] Matrix;
    - Test on Provided [end] index.

    Args:
    - @df, dist, start, end

    Outputs:
    - The Routing Table.
    '''

    n = len(df)

    assert(n > 3)

    d = df.values.copy()
    if dist is None:
        dist = np.zeros((n, n))
        for j in range(n):
            dist[j] = np.linalg.norm(d - d[j], axis=1)
            dist[j][j] = np.inf

    df['state'] = 'outside'
    route = []

    j = np.argmin(dist[start])
    route.append((start, j))
    df.loc[start, 'state'] = 'inside'
    df.loc[j, 'state'] = 'inside'

    if j == end:
        return route, dist

    for _ in tqdm(range(n)):
        inside = df.query('state=="inside"').index
        outside = df.query('state=="outside"').index
        _dist = dist[inside][:, outside]
        a, b = np.unravel_index(np.argmin(_dist), _dist.shape)
        a, b = inside[a], outside[b]
        route.append((a, b))
        df.loc[a, 'state'] = 'inside'
        df.loc[b, 'state'] = 'inside'

        if b == end:
            print('I: Break Adding because End is Reached.')
            break

        if 'outside' not in df['state'].values:
            print('I: Break Adding because No Node is Left.')
            break

    return route, dist


# %%
route, dist = mk_route_least_length(nodes.copy())

# %%
clustering = SpectralClustering(n_clusters=15,
                                affinity='precomputed',
                                assign_labels='discretize')

_dist = dist.copy()
_dist[dist == np.inf] = 0

_map = dist > -1
for r in route:
    _map[r[0], r[1]] = False
    _map[r[1], r[0]] = False
_map
_dist[_map] = 0

label = clustering.fit_predict(_dist)

# %%

links = []
for j, r in enumerate(route):
    a = nodes.loc[r[0]]
    b = nodes.loc[r[1]]
    l = str(label[r[0]])
    nodes.loc[r[0], 'label'] = l
    nodes.loc[r[1], 'label'] = l
    links.append((a[0], a[1], j, l))
    links.append((b[0], b[1], j, l))

nodes['name'] = df_all['name']
links = pd.DataFrame(links, columns=['x', 'y', 'group', 'label'])

# %%
size_kwargs = dict(
    width=600,
    height=500
)
fig1 = px.scatter(nodes, x='x', y='y', hover_name='name',
                  color='label', title='Scatter Plot', **size_kwargs)
fig1.show()
fig2 = px.line(links, x='x', y='y', line_group='group',
               color='label', **size_kwargs)
fig2.show()

# %%
fig = go.Figure()

for d in fig1.data:
    d['marker']['opacity'] = 0.2
    d['marker']['color'] = 'gray'
    fig.add_trace(d)

for d in fig2.data:
    fig.add_trace(d)

fig.update_layout({'title': 'Least Length Route',
                   'width': 600, 'height': 500})
fig.show()

# %%

# %%


def mk_routeDict(route):
    '''
    Method: mk_routeDict

    Make Dict of Route [route]

    Args:
    - @route

    Outputs:
    - The Dict

    '''

    rd = dict()
    for r in route:
        assert(r[1] not in rd)
        rd[r[1]] = r[0]

    return rd


def trace_route(start, end, rd):
    '''
    Method: trace_route

    Trace the Length from [start] to [end],
    using the Route Dict [rd]

    Args:
    - @start, end, rd

    Outputs:
    - The Length

    '''

    if start == end:
        return [start]

    trace0 = [start]
    while True:
        if trace0[-1] not in rd:
            break
        trace0.append(rd[trace0[-1]])

    trace1 = [end]
    while True:
        if trace1[-1] not in rd:
            break
        trace1.append(rd[trace1[-1]])

    x = []
    while True:
        if not trace0:
            break
        if not trace1:
            break
        if trace0[-1] == trace1[-1]:
            trace0.pop(-1)
            x = [trace1.pop(-1)]
        else:
            break

    return trace0 + x + trace1[::-1]


# %%
rd = mk_routeDict(route)

# %%
a, b = [np.random.randint(0, len(nodes)) for _ in range(2)]
trace = trace_route(a, b, rd)
print(trace[0], trace[-1], len(trace))

_nodes = nodes.loc[trace]
_nodes['name'] = _nodes.index
fig11 = px.scatter(_nodes, x='x', y='y', text='name')

fig2 = px.line(links, x='x', y='y', line_group='group', color='label')

fig = go.Figure()

for d in fig11.data:
    fig.add_trace(d)

for d in fig2.data:
    fig.add_trace(d)

fig.update_layout({'title': 'Least Length Route {} -> {}'.format(a, b)})
fig.show()

# %%
n = len(nodes)
dist_graph = np.zeros((n, n))
for a in tqdm(range(n)):
    for b in range(n):
        dist_graph[a][b] = len(trace_route(a, b, rd))

dist_graph

# %%
fig = px.histogram(dist_graph.ravel(), title='Histogram of Distance in Graph')
fig.show()

# %%
