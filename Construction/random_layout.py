'''
FileName: random_layout.py
Author: Chuncheng
Version: V0.0
Purpose: Random Layout the Road Nodes
'''

# %%
from settings import *

# %%
data = np.random.randint(0, 100, (Num, 2))
data.shape

# %%
p = os.path.join(MiddleFolder, 'nodes.json')
df = pd.DataFrame(data)
df.columns = ['x', 'y']
df.to_json(p)
print(f'D: Nodes Layout is Saved at {p}.')
df

# %%
# This block will generate scatter plots on Jupyter-like script.
px.scatter(df, x='x', y='y', title='Scatter Plot')

# %%
