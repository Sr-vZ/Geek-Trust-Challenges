import plotly
import plotly.graph_objects as go
import networkx as nx
import pandas as pd
import numpy as np
import random

# Prepare Data
G = nx.Graph()
data = pd.read_excel('books.xlsx')
data = data.sort_values(by=['Publication_Year', 'Title', 'ID'])

for index, row in data.iterrows():
    G.add_node(data['Title'][index], value=data['Publication_Year'][index], id=data['ID'][index])
    # print([data['ID'][index], data['Commentary_IDs'][index]])
    e = []
    # print(data['Commentary_IDs'][index], type(data['Commentary_IDs'][index]))
    if data['Commentary_IDs'][index] not in ['Nothing', 'nothing'] and isinstance(data['Commentary_IDs'][index], str):
        for n in data['Commentary_IDs'][index].split(','):
            e.append((data['Title'][index], data.loc[data['ID'] == int(n), 'Title'].item()))
    elif isinstance(data['Commentary_IDs'][index], int):
        e.append((data['Title'][index], data.loc[data['ID'] == data['Commentary_IDs'][index], 'Title'].item()))
    if len(e) > 0:
        # print(e)
        G.add_edges_from(e)

# sorted(G.degree, key=lambda x: x[1], reverse=True)

pos = nx.spring_layout(G, k=.5*1/np.sqrt(len(G.nodes())), iterations=500, scale=1)
other_y = nx.get_node_attributes(G, 'value')
other_x = nx.get_node_attributes(G, 'id')
i = 0
posX = []
posY = []
val = []
source = []
target = []
labels = []
yScale = data['Publication_Year'].max() - (data['Publication_Year'].min())
xScale = data['ID'].max()
eqX = np.linspace(0.0, 1.0, len(G.nodes()), True)
edges = list(G.edges())
for node, node_pos in pos.items():
    if node in other_y.keys():
        pos_ = pos[node]
        # pos_ = list(pos[node])
        pos_[1] = other_y[node]
        # if i%2 == 0:
        #     x = 100
        # else:
        #     x = 200
        # pos_[0] = other_x[node]
        # pos_[0] = i
        pos[node] = pos_
        # pos[node] = tuple(pos_)
        
        labels.append(node)
        posY.append(round(random.uniform(0.0,1.0), 4))
        posX.append((other_y[node]+abs(data['Publication_Year'].min()))/yScale)
        for e in edges:
            e = list(e)
            if node == e[0]:
                source.append(i)
            elif node == e[1]:
                target.append(i)
        i=i+1
        val.append(1)
        print(node, node_pos, pos[node],other_y[node])

# print(pos)
# fig = go.Figure(go.Sankey(
#     arrangement = "snap",
#     node = {
#         "label": ["A", "B", "C", "D", "E", "F"],
#         "x": [0.2, 0.1, 0.5, 0.7, 0.3, 0.5],
#         "y": [0.7, 0.5, 0.2, 0.4, 0.2, 0.3],
#         'pad':10},  # 10 Pixels 
#     link = {
#         "source": [0, 0, 1, 2, 5, 4, 3, 5],
#         "target": [5, 3, 4, 3, 0, 2, 2, 3],
#         "value": [1, 2, 1, 1, 1, 1, 1, 2]}))
fig = go.Figure(go.Sankey(
    arrangement = "fixed",
    node = {
        "label": labels,
        "x": posX,
        "y": posY,
        'pad':10},  # 10 Pixels 
    link = {
        "source": source,
        "target": target,
        "value": val}))
plotly.offline.plot(fig, filename='name.html')
# fig.show()