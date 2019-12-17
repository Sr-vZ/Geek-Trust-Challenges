import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import networkx as nx
import numpy as np

warnings.filterwarnings(action='once')

large = 22
med = 16
small = 12
params = {'axes.titlesize': large,
          'legend.fontsize': med,
          'figure.figsize': (16, 10),
          'axes.labelsize': med,
          'axes.titlesize': med,
          'xtick.labelsize': med,
          'ytick.labelsize': med,
          'figure.titlesize': large}
plt.rcParams.update(params)
plt.style.use('seaborn-whitegrid')
sns.set_style("white")
# %matplotlib inline

# Version
print(mpl.__version__)  # > 3.0.0
print(sns.__version__)  # > 0.9.0
data = pd.read_excel('books.xlsx')
print(data.loc[data['ID'] == 1283, 'Title'])
print(data.head())
G = nx.Graph()
for index, row in data.iterrows():
    G.add_node(data['Title'][index], value=data['Publication_Year'][index])
    # print([data['ID'][index], data['Commentary_IDs'][index]])
    e = []
    # print(data['Commentary_IDs'][index], type(data['Commentary_IDs'][index]))
    if data['Commentary_IDs'][index] not in ['Nothing','nothing'] and isinstance(data['Commentary_IDs'][index], str):
        for n in data['Commentary_IDs'][index].split(','):
            e.append((data['Title'][index], data.loc[data['ID'] == int(n), 'Title'].item()))
    elif isinstance(data['Commentary_IDs'][index], int):
        e.append((data['Title'][index], data.loc[data['ID'] == data['Commentary_IDs'][index], 'Title'].item()))
    if len(e)>0:        
        # print(e)
        G.add_edges_from(e)

# filtredData = pd.DataFrame([data['Publication_Year'], data['Title']])
data = data.sort_values(by='Publication_Year', ascending=False)
filtredData = [data['Publication_Year'], data['ID']]
# filtredData.plot()
# print(data['Commentary_IDs'][122])
# plt.scatter(filtredData[1], filtredData[0], marker='o', color="red")
pos = nx.spring_layout(G, k=5*1/np.sqrt(len(G.nodes())), iterations=20)
# pos = nx.spring_layout(G)  # default layout like in your code
fig, ax = plt.subplots(figsize=(25, 15))
# other_y = nx.get_node_attributes(G, 'value')
# for node, node_pos in pos.items():
#     if node in other_y.keys():
#         pos_ = pos[node]
#         pos_[1] = other_y[node]
#         pos[node] = pos_

other_x = nx.get_node_attributes(G, 'value')
for node, node_pos in pos.items():
    if node in other_x.keys():
        pos_ = pos[node]
        pos_[0] = other_x[node]
        pos[node] = pos_

nx.draw(G, pos=pos, ax=ax)
nx.draw_networkx_labels(G, pos=pos)
# nx.draw(G, with_labels=True, font_weight='bold')
ax.set_axis_on()
ax.tick_params(bottom=True, labelbottom=True)
plt.show()
