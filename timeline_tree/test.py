import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import seaborn as sns
import warnings
import networkx as nx
import numpy as np
import bezier
from fa2 import ForceAtlas2


def curved_edges(G, pos, dist_ratio=0.2, bezier_precision=20, polarity='random'):
    # Get nodes into np array
    edges = np.array(G.edges())
    l = edges.shape[0]

    if polarity == 'random':
        # Random polarity of curve
        rnd = np.where(np.random.randint(2, size=l) == 0, -1, 1)
    else:
        # Create a fixed (hashed) polarity column in the case we use fixed polarity
        # This is useful, e.g., for animations
        rnd = np.where(np.mod(np.vectorize(hash)(
            edges[:, 0])+np.vectorize(hash)(edges[:, 1]), 2) == 0, -1, 1)

    # Coordinates (x,y) of both nodes for each edge
    # e.g., https://stackoverflow.com/questions/16992713/translate-every-element-in-numpy-array-according-to-key
    # Note the np.vectorize method doesn't work for all node position dictionaries for some reason
    u, inv = np.unique(edges, return_inverse=True)
    coords = np.array([pos[x] for x in u])[inv].reshape(
        [edges.shape[0], 2, edges.shape[1]])
    coords_node1 = coords[:, 0, :]
    coords_node2 = coords[:, 1, :]

    # Swap node1/node2 allocations to make sure the directionality works correctly
    should_swap = coords_node1[:, 0] > coords_node2[:, 0]
    coords_node1[should_swap], coords_node2[should_swap] = coords_node2[should_swap], coords_node1[should_swap]

    # Distance for control points
    dist = dist_ratio * np.sqrt(np.sum((coords_node1-coords_node2)**2, axis=1))

    # Gradients of line connecting node & perpendicular
    m1 = (coords_node2[:, 1]-coords_node1[:, 1]) / \
        (coords_node2[:, 0]-coords_node1[:, 0])
    m2 = -1/m1

    # Temporary points along the line which connects two nodes
    # e.g., https://math.stackexchange.com/questions/656500/given-a-point-slope-and-a-distance-along-that-slope-easily-find-a-second-p
    t1 = dist/np.sqrt(1+m1**2)
    v1 = np.array([np.ones(l), m1])
    coords_node1_displace = coords_node1 + (v1*t1).T
    coords_node2_displace = coords_node2 - (v1*t1).T

    # Control points, same distance but along perpendicular line
    # rnd gives the 'polarity' to determine which side of the line the curve should arc
    t2 = dist/np.sqrt(1+m2**2)
    v2 = np.array([np.ones(len(edges)), m2])
    coords_node1_ctrl = coords_node1_displace + (rnd*v2*t2).T
    coords_node2_ctrl = coords_node2_displace + (rnd*v2*t2).T

    # Combine all these four (x,y) columns into a 'node matrix'
    node_matrix = np.array(
        [coords_node1, coords_node1_ctrl, coords_node2_ctrl, coords_node2])

    # Create the Bezier curves and store them in a list
    curveplots = []
    for i in range(l):
        nodes = node_matrix[:, i, :].T
        curveplots.append(bezier.Curve(nodes, degree=2).evaluate_multi(
            np.linspace(0, 1, bezier_precision)).T)

    # Return an array of these curves
    curves = np.array(curveplots)
    return curves


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
# G = nx.DiGraph()
data = data.sort_values(by=['Publication_Year','Title','ID'], ascending=False)


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
pos = nx.spring_layout(G, k=100*1/np.sqrt(len(G.nodes())), iterations=2000, scale=10)
# pos = nx.spiral_layout(G)
# print(pos)
# pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
forceatlas2 = ForceAtlas2()
forceatlas2 = ForceAtlas2(
                        # Behavior alternatives
                        outboundAttractionDistribution=False,  # Dissuade hubs
                        linLogMode=False,  # NOT IMPLEMENTED
                        adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
                        edgeWeightInfluence=1.0,

                        # Performance
                        jitterTolerance=0.1,  # Tolerance
                        barnesHutOptimize=True,
                        barnesHutTheta=1.2,
                        multiThreaded=False,  # NOT IMPLEMENTED

                        # Tuning
                        scalingRatio=5.0,
                        strongGravityMode=False,
                        gravity=0.01,

                        # Log
                        verbose=True)
# pos = forceatlas2.forceatlas2_networkx_layout(G, pos=None, iterations=1000)
# pos = nx.spring_layout(G)  # default layout like in your code
# fig, ax = plt.subplots(figsize=(200, 200))
# fig, ax = plt.subplots()
fig, ay = plt.subplots()
# other_y = nx.get_node_attributes(G, 'value')
# for node, node_pos in pos.items():
#     if node in other_y.keys():
#         pos_ = pos[node]
#         pos_[1] = other_y[node]
#         pos[node] = pos_

other_x = nx.get_node_attributes(G, 'value')
for node, node_pos in pos.items():
    if node in other_x.keys():
        # pos_ = pos[node]
        pos_ = list(pos[node])
        pos_[1] = other_x[node]
        # pos[node] = pos_
        pos[node] = tuple(pos_)
# print(other_x)
# print(pos)
# nx.draw(G, pos=pos, ax=ax)

# Produce the curves
# curves = curved_edges(G, pos)
# lc = LineCollection(curves, color='black', alpha=0.2)

# nx.draw(G, pos=pos, width=0.2, node_color='skyblue', ax=ax)
nx.draw(G, pos=pos, width=0.2, node_color='skyblue', ay=ay)
# nx.draw_networkx_nodes(G, pos=pos, node_size=10, node_color='skyblue', alpha=1)
# nx.draw_networkx_edges(G, pos=pos, width=0.2)
print(G.edges)
# nx.draw(G, nx.graphviz_layout(G, prog='dot'))
# nx.draw_networkx_nodes(G, pos, node_size=10, node_color='skyblue', alpha=1)
# nx.draw_networkx_edges(G, pos=nx.spring_layout(G))
# plt.gca().add_collection(lc)
# plt.tick_params(axis='both',which='both',bottom=True,left=False,labelbottom=True,labelleft=False)

nx.draw_networkx_labels(G, pos=pos, font_size=8)
# nx.draw(G, with_labels=True, font_weight='bold')
# ax.set_axis_on()
# ax.tick_params(bottom=True, labelbottom=True)
ay.set_axis_on()
ay.tick_params(left=True, labelleft=True)
plt.show()
