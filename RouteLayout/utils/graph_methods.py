'''
FileName: graph_methods.py
Author: Chuncheng
Version: V0.0
Purpose: Provide Methods for Graph Theory Computation
'''

from .deploy import *


class PathSeacher(object):
    ''' Path Seacher for the Nodes in a Graph.
    It will search and record the shortest path between nodes.
    '''

    def __init__(self):
        self.memory = dict()
        pass

    def trace_all(self, dist):
        '''
        Method: trace_all

        Trace the shortest path between each Nodes.
        The distance matrix of the nodes is [dist],
        the edge can not be visited should be valued as a large value in advance,
        like np.inf.

        Args:
        - @self, dist

        Outputs:
        - The distance matrix of the Graph using Shortest Path Length

        '''

        n = len(dist)
        self.dist = dist

        Info('Trace all Nodes Pairs of {} x {} sized Graph'.format(n, n))

        m = np.zeros((n, n))

        for a in tqdm(range(n)):
            for b in range(a):
                t = self.memory.get((a, b), self.trace(a, b))
                m[a][b] = len(t)

        return m

    def trace(self, start, end, dist=None):
        '''
        Method: trace

        Trace the shortest path between nodes of [start] and [end],
        the [dist] is the distance matrix,
        if it is None, we will use self.dist instead.

        During Tracing,
        the self.memory is updated to pervent repeat computation.

        Args:
        - @self, start, dist=None

        Outputs:
        - The trace as links, a list of edges

        '''

        if dist is None:
            dist = self.dist

        inside = [start]
        outside = [e for e in range(len(dist)) if not e == start]

        trace = dict()

        accum = np.zeros(dist.shape)

        def trace_back(e):
            back = [e]
            while back[-1] != start:
                back.append(trace[back[-1]])
            return back[::-1]

        for ____ in dist:
            x = dist + accum
            _dist = x[inside][:, outside]
            a, b = np.unravel_index(np.argmin(_dist), _dist.shape)
            a, b = inside[a], outside[b]
            trace[b] = a
            inside.append(b)
            outside.remove(b)
            accum[b, :] = x[a, b]
            if b == end:
                break
            if len(outside) == 0:
                break

        tbr = trace_back(end)

        # Debug('Traced from {} to {} for {} Jumps'.format(start, end, len(tbr)))

        tb = tbr.copy()
        while len(tb):
            for j in range(len(tb)-1):
                self.memory[(tb[j], tb[-1])] = tb[j:]

            for j in range(1, len(tb)):
                self.memory[(tb[0], tb[j])] = tb[:j+1]

            tb = tb[1:-1]

        # Debug('Updated Memory to {} entries'.format(len(self.memory)))

        out = []
        for j in range(len(tbr)-1):
            out.append((tbr[j], tbr[j+1]))

        return out


@Timer
def compute_dist(nodes, columns=['x', 'y'], diag=0):
    '''
    Method: compute_dist

    Compute the Distance Matrix of Nodes [nodes]

    Args:
    - @nodes: The Nodes as DataFrame;
    - @columns=['x', 'y']: The Position Column of Coordinates;
    - @diag=0: The Diagonal of the Distance Matrix, Keep Unchanged if is None.

    Outputs:
    - The Distance Matrix

    '''

    d = nodes[columns].values
    n = d.shape[0]

    if n < 3:
        Error('Too Few Nodes ({}) is Provided'.format(n))
        raise ValueError('NotEnoughNodes')

    Debug('Got {} nodes in columns of {}'.format(n, columns))

    dist = np.zeros((n, n))
    for j in tqdm(range(n)):
        dist[j] = np.linalg.norm(d - d[j], axis=1)
        if not diag is None:
            dist[j][j] = diag

    Debug('Computed Distance Matrix as ({} x {})'.format(n, n))

    return dist


@Timer
def mask_dist(dist, links, mode='mask_unlink', mask_value=0, add_reverse=True):
    '''
    Method: mask_dist

    Mask the Distance Matrix with Links,
    to Mask Unlinked or Linked Edges, as the option of [mode].

    Args:
    - @dist: The Distance Matrix;
    - @links: The Links (or Edges);
    - @mode='mask_unlink': The Mode of Masking;
                       - 'mask_unlink' means we only block the Edges of Un-linked Nodes;
                       - Otherwise means we mask the Edges of Linked Nodes.
    - @mask_value=0: The Mask Value;
    - @add_reverse=True: The Switcher if Add Reverse Link for each Edge.

    Outputs:
    - The Masked Distance Matrix

    '''

    uniques = set(e for e in links)
    Info('Masking with {}|{} Edges'.format(len(uniques), len(links)))

    _map = np.zeros(dist.shape)
    for e in tqdm(uniques):
        _map[e[0], e[1]] = 1
        if add_reverse:
            _map[e[1], e[0]] = 1

    mdist = dist.copy()
    if mode == 'mask_unlink':
        mdist[_map == 0] = mask_value
    elif mode == 'mask_link':
        mdist[_map == 1] = mask_value
    else:
        raise ValueError('Invalid Mode of {}'.format(mode))

    Info('Masked {} Values in Distance Matrix'.format(np.sum(1 - _map)))

    return mdist


@Timer
def spectral_clustering(dist, n_clusters=4):
    '''
    Method: spectral_clustering

    Compute Spectral Clustering of Distance Matrix

    Args:
    - @dist: The Distance Matrix;
    - @n_clusters=4: The Number of Clustering.

    Outputs:
    - The Labels of Clustering.

    '''

    clustering = SpectralClustering(n_clusters=n_clusters,
                                    affinity='precomputed',
                                    assign_labels='discretize')

    label = clustering.fit_predict(dist)
    Info('Clustered {} clusters, for dist shape of {}'.format(n_clusters, dist.shape))
    return label
