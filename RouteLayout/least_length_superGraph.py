'''
FileName: least_length_superGraph.py
Author: Chuncheng
Version: V0.0
Purpose: Improved Least Length Analysis,
         the Super Node Graph is Implemented to Solve Trace Dependency
'''

# %%
from sklearn.cluster import SpectralClustering
from settings import *

# %%

# ------------------------------------------------------
# Functions
# ------------------------------------------------------


@timer
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


def spectral_clustering(dist, route):
    '''
    Method: spectral_clustering

    Spectral Clustering with [dist] and [route]

    Args:
    - @dist: The Distance Matrix;
    - @route: The Routing Map.

    Outputs:
    - The Labels

    '''

    clustering = SpectralClustering(n_clusters=4,
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

    return label


def plot_routing(nodes, route, label):
    '''
    Method: plot_routing

    Plot the Nodes with Routing

    Args:
    - @nodes, route, label

    Outputs:
    - The Links of the Routing

    '''

    # Make Links Table of the Routing

    links = []
    for j, r in enumerate(route):
        a = nodes.loc[r[0]]
        b = nodes.loc[r[1]]
        l = str(label[r[0]])
        nodes.loc[r[0], 'label'] = l
        nodes.loc[r[1], 'label'] = l
        links.append((a[0], a[1], j, l))
        links.append((b[0], b[1], j, l))

    nodes['name'] = nodes.index

    links = pd.DataFrame(links, columns=['x', 'y', 'group', 'label'])

    # Plot the Least Legnth Routing Figures
    fig1 = px.scatter(nodes, x='x', y='y', color='label',
                      hover_name='name', title='Scatter Plot')
    # fig1.show()
    fig2 = px.line(links, x='x', y='y', line_group='group', color='label')
    # fig2.show()

    fig = go.Figure()
    for d in fig1.data:
        fig.add_trace(d)
    for d in fig2.data:
        fig.add_trace(d)
    fig.update_layout({'title': 'Least Length Route'})
    fig.show()

    return links


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
# ------------------------------------------------------
# Load the Nodes
# ------------------------------------------------------


nodes = pd.read_json(os.path.join(MiddleFolder, 'nodes.json'))
nodes

# %%
# ------------------------------------------------------
# Routing and Labeling
# ------------------------------------------------------

# Estimate the Least Length Routing,
# and the Distance Matrix is computed
route, dist = mk_route_least_length(nodes.copy())

# %%
# Spectral Clustering based on the Dist and Routing
label = spectral_clustering(dist, route)

# %%
plot_routing(nodes, route, label)

# %%
nodes

# %%
# ------------------------------------------------------
# Estimate Distances
# ------------------------------------------------------

# Estimate the Path Distances between Each Two Nodes
rd = mk_routeDict(route)
n = len(nodes)
dist_graph = np.zeros((n, n))
for a in tqdm(range(n)):
    for b in range(n):
        t = trace_route(a, b, rd)
        dist_graph[a][b] = len(t)
        # if len(t) == 1:
        #     dist_graph[a][b] = 0
        # else:
        #     s = np.sum(dist[t[j]][t[j+1]] for j in range(len(t)-1))
        #     dist_graph[a][b] = s

dist_graph

# %%
_nodes = nodes.copy()
_route = route.copy()
_dist = dist.copy() - dist_graph

while len(_nodes['label'].unique()) > 1:

    for j in tqdm(_nodes.index):
        l = _nodes.loc[j, 'label']
        ks = _nodes.query('label=="{}"'.format(l)).index
        _dist[j, ks] = np.inf
    print()

    a, b = np.unravel_index(np.argmin(_dist), _dist.shape)

    if (a, b) in _route or (b, a) in _route:
        _dist[a, b] = np.inf
        _dist[b, a] = np.inf
        continue

    la, lb = _nodes.loc[[a, b], 'label']
    print('D: Linked Nodes {} -> {}'.format(a, b))
    _route.append((a, b))

    def foo(e):
        if e == lb:
            return la
        else:
            return e

    _nodes['label'] = _nodes['label'].map(foo)

    print('D: Linked Label {} -> {}'.format(lb, la))

new_route = _route

# %%
links = plot_routing(nodes, new_route, label)

# %%

memory = [pd.DataFrame(columns=['pair', 'dist'])]


# @timer
def shortest_trace(start, end, new_dist):
    '''
    Method: shortest_trace

    Compute  the Shortest Trace of the Common Graph

    Args:
    - @start, end, new_dist

    Outputs:
    - The Computed Trace

    '''
    _dist = new_dist.copy()

    n = len(_dist)

    df = nodes.copy()
    trace = dict()

    df['state'] = 'outside'
    df.loc[start, 'state'] = 'inside'

    accum = np.zeros((n, n))

    def trace_back(e):
        back = [e]
        while back[-1] != start:
            back.append(trace[back[-1]])
        return back

    for ____ in nodes.index:
        inside = df.query('state=="inside"').index
        outside = df.query('state=="outside"').index
        x = _dist + accum
        __dist = x[inside][:, outside]
        a, b = np.unravel_index(np.argmin(__dist), __dist.shape)
        a, b = inside[a], outside[b]
        trace[b] = a
        df.loc[a, 'state'] = 'inside'
        df.loc[b, 'state'] = 'inside'
        d = x[a, b]
        accum[b, :] = d

        if not (start, b) in list(memory[0]['pair']):
            memory[0] = memory[0].append(dict(
                pair=(start, b),
                dist=len(trace_back(b))
            ), ignore_index=True)

        if not (b, start) in list(memory[0]['pair']):
            memory[0] = memory[0].append(dict(
                pair=(b, start),
                dist=len(trace_back(b))
            ), ignore_index=True)

        if end == b:
            break

    print(len(memory[0]))

    return trace_back(end)


# %%

a, b = [np.random.randint(0, len(nodes)) for _ in range(2)]
# a, b = 75, 63

_map = dist * 0
for r in new_route:
    _map[r[0], r[1]] = 1
    _map[r[1], r[0]] = 1

_dist = dist.copy()
_dist[_map == 0] = np.inf

trace = shortest_trace(a, b, _dist)
print(len(trace))

_nodes = nodes.loc[trace]
_nodes['name'] = _nodes.index
fig11 = px.scatter(_nodes, x='x', y='y', text='name')

fig2 = px.line(links, x='x', y='y', line_group='group', color='label')

fig = go.Figure()

for d in fig11.data:
    fig.add_trace(d)

for d in fig2.data:
    d['line']['width'] = 0.5
    fig.add_trace(d)

fig.update_layout({'title': 'Least Length Route {} -> {}'.format(a, b)})
fig.show()

# memory[0]

# %%
# ------------------------------------------------------
# Estimate Distances
# ------------------------------------------------------

# Estimate the Path Distances between Each Two Nodes
n = len(nodes)
dist_graph = np.zeros((n, n))
for a in tqdm(range(n)):
    for b in range(a):
        if (a, b) in list(memory[0]['pair']):
            d = memory[0][memory[0]['pair'] == (a, b)]['dist'].iloc[0]
        else:
            d = len(shortest_trace(a, b, _dist))
        dist_graph[a][b] = d

dist_graph

# %%
# Separate Within- and Across-Labels Distances
across = []
within = []

n = len(nodes)

for j in range(n):
    for k in range(j):

        v = dist_graph[j, k]

        if nodes['label'][j] == nodes['label'][k]:
            within.append(v)
        else:
            across.append(v)

# %%
# Plot Histogram of the Distances
df1 = pd.DataFrame(within)
df1.columns = ['y']
df1['name'] = 'within'

df2 = pd.DataFrame(across)
df2.columns = ['y']
df2['name'] = 'across'

df = pd.concat([df1, df2], axis=0, ignore_index=True)

fig = px.histogram(df, x='y', color='name', opacity=0.8,
                   title='Histogram of Separation')
fig.show()

# %%
dump_middle('_hist_sparate_improve.dump', (df1, df2))

# %%
