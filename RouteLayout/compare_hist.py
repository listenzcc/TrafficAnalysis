'''
FileName: compare_hist.py
Author: Chuncheng
Version: V0.0
Purpose: Compare Histogram os Graphs
'''

# %%
from settings import *

# %%
a_df1, a_df2 = load_middle('_hist_sparate_improve.dump')
a_df1['name'] = a_df1['name'].map(lambda e: 'shortCut_{}'.format(e))
a_df2['name'] = a_df2['name'].map(lambda e: 'shortCut_{}'.format(e))

# %%
b_df1, b_df2 = load_middle('_hist_sparate_trivial.dump')
b_df1['name'] = b_df1['name'].map(lambda e: 'trivial_{}'.format(e))
b_df2['name'] = b_df2['name'].map(lambda e: 'trivial_{}'.format(e))

# %%
df = pd.concat([a_df1, a_df2, b_df1, b_df2], axis=0, ignore_index=True)

fig = px.histogram(df, x='y', color='name', opacity=0.8, barmode='overlay',
                   title='Histogram Compare')
fig.show()

# %%
for e in [a_df1, a_df2, b_df1, b_df2]:
    print(len(e))

# %%
