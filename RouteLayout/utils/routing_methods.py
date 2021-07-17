'''
FileName: routing_methods.py
Author: Chuncheng
Version: V0.0
Purpose: The Method of Computing the Routings of the Nodes
'''

from .deploy import *


@Timer
def route_between_labels(nodes, dist, labels):
    '''
    Method: route_between_labels

    Routing Nodes Between Labels.

    Args:
    - @nodes, dist, labels

    Outputs:
    - The Links between Labels

    '''

    _nodes = nodes.copy()
    _dist = dist.copy()

    n = len(nodes)
    uniques = np.unique(labels)
    Debug('Routing Between Labels with {} Nodes and {} Labels'.format(
        n, len(uniques)))

    for a in range(n):
        for b in range(n):
            if labels[a] == labels[b]:
                _dist[a, b] = np.inf

    _nodes['label'] = labels
    _nodes['label'] = _nodes['label'].map(str)

    links = []

    while len(_nodes['label'].unique()) > 1:
        # Block All the Same-Label Edges
        for j in _nodes.index:
            l = _nodes.loc[j, 'label']
            ks = _nodes.query('label=="{}"'.format(l)).index
            _dist[j, ks] = np.inf
            _dist[ks, j] = np.inf

        a, b = np.unravel_index(np.argmin(_dist), _dist.shape)

        la, lb = _nodes.loc[[a, b], 'label']

        def foo(e):
            if e == lb:
                return la
            else:
                return e

        _nodes['label'] = _nodes['label'].map(foo)
        print(_nodes['label'].unique())

        links.append((a, b))
        Debug('D: Linked Nodes {}({}) -> {}({}), {}'.format(
            a, la, b, lb, _dist[a, b]))

    return links


@Timer
def route_least_length(dist, start=0):
    '''
    Method: route_least_length

    Compute Routing of the Nodes with Least Length Principle using Greedy Algorithm,
    in which the Distance Matrix [dist] between the Nodes is required,

    The List of the Edges in the Routing is Computed and Returned.

    The Routing Link is Started with [Start],
    which is the Index of a Node.

    Args:
    - @dist: The Distance Matrix;
    - @start: The Index of the Start Node.

    Outputs:
    - @links: The List of the Edges of the Routing;
    - @dist: The Distance Matrix in Case it is Computed.

    '''

    n = len(dist)

    # Fail on Not Enough Nodes
    if not n > 3:
        Error('I Do Not Handle Nodes less than 3')
        return None

    # Prepare Routing
    links = []

    inside = [start]
    outside = [e for e in range(n) if not e == start]

    Debug('Started Routing with {}'.format(start))

    # Routing with Greedy Algorithm
    # At the worst, we will loop n times.
    for _ in tqdm(range(n)):
        _dist = dist[inside][:, outside]
        a, b = np.unravel_index(np.argmin(_dist), _dist.shape)
        a, b = inside[a], outside[b]
        links.append((a, b))
        inside.append(b)
        outside.remove(b)
        if len(outside) == 0:
            Debug('Break Loop because the outside set is empty.')
            break

    Debug('Done Routing for {} Nodes'.format(n))

    return links
