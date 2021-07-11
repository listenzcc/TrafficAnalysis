'''
FileName: route_nodes.py
Author: Chuncheng
Version: V0.0
Purpose: Compute Routing of the Nodes
'''

from .deploy import *


@Timer
def plot_routing(nodes, route, title='Routing'):
    '''
    Method: plot_routing

    Plot the Routing [route] of the Nodes [nodes]

    The Plotly Plotting Method is Called,
    and the Fig of Plotly is returned.

    The Title of the Plot is [title].

    Args:
    - @nodes, route

    Outputs:
    - The Fig

    '''

    links = []
    for j, r in enumerate(route):
        a = nodes.loc[r[0]]
        b = nodes.loc[r[1]]
        links.append((a[0], a[1], j))
        links.append((b[0], b[1], j))

    links = pd.DataFrame(links, columns=['x', 'y', 'line_group'])

    fig1 = px.scatter(nodes, x='x', y='y', hover_name='name')
    fig2 = px.line(links, x='x', y='y', line_group='line_group')
    fig2.show()

    fig = go.Figure()

    for d in fig1.data:
        d['marker']['opacity'] = 0.2
        d['marker']['color'] = 'gray'
        fig.add_trace(d)

    for d in fig2.data:
        fig.add_trace(d)

    fig.update_layout(dict(title=title))
    fig.show()

    return fig


@Timer
def route_least_length(nodes, start=0, dist=None):
    '''
    Method: route_least_length

    Compute Routing of the [nodes] with Least Length Principle using Greedy Algorithm,
    in which the Distance Matrix [dist] between the Nodes is required,
    - The provided dist matrix is used;
    - The dist is computed if not provided.

    The List of the Edges in the Routing is Computed and Returned.

    The Routing Link is Started with [Start],
    which is the Index of a Node.

    Args:
    - @nodes, dist=None

    Outputs:
    - @route: The List of the Edges of the Routing;
    - @dist: The Distance Matrix in Case it is Computed.

    '''

    n = len(nodes)

    # Fail on Not Enough Nodes
    if not n > 3:
        Error('I Do Not Handle Nodes less than 3')
        return None

    # Compute Distance Matrix
    if dist is None:
        d = nodes[['x', 'y']].values.copy()
        dist = np.zeros((n, n))
        for j in range(n):
            dist[j] = np.linalg.norm(d - d[j], axis=1)
            dist[j][j] = np.inf
        Info('Computed the Distance Matrix, since it is Not Provided')
    else:
        Info('Using the Given Distance Matrix.')

    # Prepare Routing
    route = []
    nodes['state'] = 'outside'

    # Start with [start]
    j = np.argmin(dist[start])
    route.append((start, j))
    nodes.loc[start, 'state'] = 'inside'
    nodes.loc[j, 'state'] = 'inside'
    Debug('Started Routing with {}'.format((start, j)))

    # Routing with Greedy Algorithm
    for _ in tqdm(range(n)):
        inside = nodes.query('state=="inside"').index
        outside = nodes.query('state=="outside"').index
        _dist = dist[inside][:, outside]
        a, b = np.unravel_index(np.argmin(_dist), _dist.shape)
        a, b = inside[a], outside[b]
        route.append((a, b))
        nodes.loc[a, 'state'] = 'inside'
        nodes.loc[b, 'state'] = 'inside'

        if 'outside' not in nodes['state'].values:
            Debug('Break Adding because No Node is Left.')
            break

    Debug('Done Routing for {} Nodes'.format(n))

    return route, dist
