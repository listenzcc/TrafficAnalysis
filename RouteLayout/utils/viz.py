'''
FileName: viz.py
Author: Chuncheng
Version: V0.0
Purpose: Visualizing Toolbox
'''

from .deploy import *


@Timer
def plot_layout(nodes, color=None, links=None, title='Default Title'):
    '''
    Method: plot_layout

    Plot the Layout of the [nodes].

    The Plotly Plotting Method is Called,
    and the Fig of Plotly is returned.

    The Title of the Plot is [title].

    Args:
    - @nodes: The DataFrame with 'x', 'y', and 'name' columns;
    - @color=None: The Color of the Nodes,
                   - None: No Color;
                   - {str}: The Column of Color;
                   - {list}: The List of Color of Each Node;
    - @links=None: The Edges to be Plotted, None refers No Plot.
    - @title='Default Title': The Title of the Figure.

    Outputs:
    - The Figure

    '''

    # Prepare Copy of Nodes
    _nodes = nodes.copy()

    # Color

    if isinstance(color, str):
        assert(color in _nodes.columns)

    elif color is None:
        _nodes['color'] = 'black'
        color = 'color'

    else:
        _nodes['color'] = color
        color = 'color'

    _nodes[color] = _nodes[color].map(str)

    fig1 = px.scatter(_nodes, x='x', y='y', hover_name='name',
                      color=color, title=title)

    Debug('Plotted {} Nodes'.format(len(_nodes)))

    if links is None:
        return fig1

    # Edges

    edges = []
    for j, e in tqdm(enumerate(set(links))):
        a = _nodes.loc[e[0]]
        b = _nodes.loc[e[1]]
        c = _nodes.loc[e[0], 'color']
        edges.append((a['x'], a['y'], c, j))
        edges.append((b['x'], b['y'], c, j))

    edges = pd.DataFrame(edges, columns=['x', 'y', 'color', 'line_group'])

    fig2 = px.line(edges, x='x', y='y', line_group='line_group', color='color')
    Debug('Plotted {} Edges'.format(len(edges)))

    fig = go.Figure()

    for d in fig1.data:
        fig.add_trace(d)

    for d in fig2.data:
        fig.add_trace(d)

    fig.update_layout({'title': title})

    return fig
