'''
FileName: layout_nodes.py
Author: Chuncheng
Version: V0.0
Purpose: Setup the Layout of the Nodes
'''


from .deploy import *


@Timer
def plot_layout(nodes, title='Layout Scatter'):
    '''
    Method: plot_layout

    Plot the Layout of the [nodes].

    The Plotly Plotting Method is Called,
    and the Fig of Plotly is returned.

    The Title of the Plot is [title].

    Args:
    - @nodes

    Outputs:
    - The Fig

    '''

    fig = px.scatter(nodes, x='x', y='y', hover_name='name', title=title)
    fig.show()

    return fig


@Timer
def layout_random(num=Num,
                  rng=(0, 100),
                  dim=2,
                  columns=['x', 'y'],
                  out_file=Path('random_layout.json')):
    '''
    Method: layout_random

    Randomly Generate [num] Nodes,
    the Range is [rng],
    the Dimension is [dim].

    The Generated Layout is Saved in [out_file] as Full-Path.

    Args:
    - @num, rng, dim, columns, out_file

    Outputs:
    - The Generated Nodes in DataFrame of Pandas

    '''

    d = np.random.randint(rng[0], rng[1], (num, dim))

    nodes = pd.DataFrame(d, columns=columns)
    nodes['name'] = nodes.index

    nodes.to_json(out_file)

    Info('Generated Random Layout on {}'.format(out_file))

    return nodes


@Timer
def layout_chinese_cities(out_file=Path('city_layout.json')):
    '''
    Method: layout_chinese_cities

    Layout Nodes as the Geography of Chinese Cities.
    The Generated Layout is Saved in [out_file] as Full-Path.

    Args:
    - @out_file

    Outputs:
    - The Generated Nodes in DataFrame of Pandas

    '''

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
            Error('Could not Find GeoJson File: {}'.format(path))
            return None
        Debug('Fetched GeoJson from {}'.format(path))

        features = gpd.GeoDataFrame.from_features(geojson['features'])
        features = pd.DataFrame(features)
        # Overwrite the Geometry to Prevent Too Large
        features['geometry'] = '--'
        Debug('Parsed Features from {}'.format(adcode))

        features = features.query('adcode != "{}"'.format(adcode))
        return features

    df = read_geojson(100000)

    dfs = []
    for code in tqdm(df['adcode'].values):
        dfs.append(read_geojson(code))

    df_all = pd.concat(dfs, axis=0)
    df_all.index = range(len(df_all))
    df_all['parent'] = df_all['parent'].map(lambda e: e['adcode'])
    df_all

    d = np.array([e for e in df_all['center'].values if isinstance(e, list)])
    nodes = pd.DataFrame(d, columns=['x', 'y'])
    nodes['name'] = nodes.index

    nodes.to_json(out_file)

    Info('Generated Random Layout on {}'.format(out_file))

    return nodes
