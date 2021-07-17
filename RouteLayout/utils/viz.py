'''
FileName: viz.py
Author: Chuncheng
Version: V0.0
Purpose: Visualizing Toolbox
'''

from .deploy import *


@Timer
def plot_layout(nodes, color=None, links=None, link_color=None, title='Default Title'):
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
    - @link_color=None: The Color of the Edges of Links;
                        - None: Same with its Node since No Link Color Specified;
                        - color: The Color of the Edges;
    - @links=None: The Edges to be Plotted, None refers No Plot.
    - @title='Default Title': The Title of the Figure.

    Outputs:
    - The Figure

    '''

    # Prepare Copy of Nodes
    _nodes = nodes.copy()

    # Plot Nodes
    if isinstance(color, str):
        # Use Column of [color] as ColorName
        assert(color in _nodes.columns)

    elif color is None:
        # Use Black Color
        _nodes['color'] = 'black'
        color = 'color'

    else:
        # Use List from Color List
        _nodes['color'] = color
        color = 'color'

    # Draw
    fig1 = px.scatter(_nodes, x='x', y='y', hover_name='name',
                      color=color, title=title)

    Debug('Plotted {} Nodes'.format(len(_nodes)))

    if links is None:
        return fig1

    # Plot Edges
    # Make up Edges,
    # the Colors are the Same as its 1st Node;
    # the lins_group is used to prevent edges from being linked one-by-one.
    edges = []
    for j, e in tqdm(enumerate(set(links))):
        a = _nodes.loc[e[0]]
        b = _nodes.loc[e[1]]
        c = _nodes.loc[e[0], 'color']
        edges.append((a['x'], a['y'], c, j))
        edges.append((b['x'], b['y'], c, j))
    edges = pd.DataFrame(edges, columns=['x', 'y', 'color', 'line_group'])

    # Draw
    # A problem is the color space is different with the Nodes

    if link_color is None:
        fig2 = px.line(edges, x='x', y='y',
                       line_group='line_group', color='color')
    else:
        fig2 = px.line(edges, x='x', y='y', line_group='line_group')
    Debug('Plotted {} Edges'.format(len(edges['line_group'].unique())))

    # Attach the Edges and Nodes to the new Figure
    fig = go.Figure()

    # Attach the Nodes and get the colors
    # The legendgroup option is to group the Nodes by the Colors
    color_table = dict()
    for j, d in enumerate(fig1.data):
        d['legendgroup'] = 'nodes - {}'.format(j)
        color_table[d['name']] = d['marker']['color']
        fig.add_trace(d)

    # Attach the Edges with the 'correct' colors
    # The legendgroup option is to group the Edges by the Colors
    for j, d in enumerate(fig2.data):
        name = d['name']
        if link_color is None:
            d['line']['color'] = color_table[name]
            d['legendgroup'] = 'edges - {}'.format(name)
        else:
            d['line']['color'] = link_color
        d['opacity'] = 0.5
        fig.add_trace(d)

    # Draw
    fig.update_layout({'title': title})

    return fig
