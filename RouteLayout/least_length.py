'''
FileName: least_length.py
Author: Chuncheng
Version: V0.0
Purpose: Layout Route by Least Length Law
'''

# %%
from settings import *

# %%
nodes = pd.read_json(os.path.join(MiddleFolder, 'nodes.json'))
nodes

# %%


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


route, dist = mk_route_least_length(nodes.copy())

# %%

links = []
for j, r in enumerate(route):
    a = nodes.loc[r[0]]
    b = nodes.loc[r[1]]
    links.append((a[0], a[1], j))
    links.append((b[0], b[1], j))

links = pd.DataFrame(links, columns=['x', 'y', 'group'])

# %%
fig1 = px.scatter(nodes, x='x', y='y', title='Scatter Plot')
fig1.show()
fig2 = px.line(links, x='x', y='y', line_group='group')

# %%
fig = go.Figure()
for d in fig1.data:
    fig.add_trace(d)
for d in fig2.data:
    fig.add_trace(d)
fig.update_layout({'title': 'Least Length Route'})
fig.show()

# %%
