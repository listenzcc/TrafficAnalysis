'''
FileName: graph_methods.py
Author: Chuncheng
Version: V0.0
Purpose: Provide Methods for Graph Theory Computation
'''

from .deploy import *


@Timer
def compute_dist_graph(links):
    '''
    Method: compute_dist_graph

    Compute Distance Matrix by Graph Distance

    Args:
    - @links

    Outputs:
    - @

    '''

    pass


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
def mask_dist(dist, links, mask_value=0, add_reverse=True):
    '''
    Method: mask_dist

    Mask the Distance Matrix with Links,
    to Only Allow Linked Edges.

    Args:
    - @dist: The Distance Matrix;
    - @links: The Links (or Edges);
    - @mask_value=0: The Mask Value;
    - @add_reverse=True: The Switcher if Add Reverse Link for each Edge.

    Outputs:
    - The Masked Distance Matrix

    '''

    uniques = set(e for e in links)
    Debug('Masking with {}|{} Edges'.format(len(uniques), len(links)))

    _map = np.zeros(dist.shape)
    for e in tqdm(uniques):
        _map[e[0], e[1]] = 1
        if add_reverse:
            _map[e[1], e[0]] = 1

    mdist = dist.copy()
    mdist[_map == 0] = mask_value
    Debug('Masked {} Values in Distance Matrix'.format(np.sum(1 - _map)))

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

    return label
