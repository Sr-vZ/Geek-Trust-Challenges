import networkx as nx
import pandas as pd
import numpy as np
from bokeh.io import show, output_file
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, BoxZoomTool, ResetTool
from bokeh.models.graphs import from_networkx
from bokeh.models import HoverTool, ColumnDataSource, LabelSet, Label
from bokeh.plotting import figure, show
from networkx.drawing.nx_pydot import write_dot
from bokeh.models.glyphs import Bezier

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

# Show with Bokeh
# plot = Plot(plot_width=900, plot_height=1200,x_range=Range1d(-10, 10), y_range=Range1d(-1.1, 1.1))
pos = nx.spring_layout(G, k=1000*1/np.sqrt(len(G.nodes())), iterations=2500, scale=5)
# pos = nx.circular_layout(G)
# nx.draw_planar(G, with_labels=True)
# pos = nx.spectral_layout(G)


other_y = nx.get_node_attributes(G, 'value')
other_x = nx.get_node_attributes(G, 'id')
i = 1
for node, node_pos in pos.items():
    if node in other_y.keys():
        pos_ = pos[node]
        # pos_ = list(pos[node])
        pos_[1] = other_y[node]
        # if i%2 == 0:
        #     x = 100
        # else:
        #     x = 200
        # pos_[0] = other_y[node]
        # pos_[0] = G.degree(node)
        # pos_[0] = i
        pos[node] = pos_
        # pos[node] = tuple(pos_)
        i=i+1
        print(node, node_pos, pos[node],other_y[node])

nodes, nodes_coordinates = zip(*sorted(pos.items()))
nodes_xs, nodes_ys = list(zip(*nodes_coordinates))
nodes_source = ColumnDataSource(dict(x=nodes_xs, y=nodes_ys, name=nodes))
# print(nodes)
# plot = Plot(plot_width=1200, plot_height=1200,x_range=Range1d(-500,500), y_range=Range1d(data['Publication_Year'].min(), data['Publication_Year'].max()))

plot = figure(plot_width=1200, plot_height=1200,tools=['tap', 'hover', 'box_zoom', 'reset'])
plot.title.text = "Graph Interaction Demonstration"
# node_hover_tool = HoverTool(tooltips=[("index", "@index"), ("club", "@club")])
# plot.add_tools(node_hover_tool, BoxZoomTool(), ResetTool())

# # graph_renderer = from_networkx(G, nx.spring_layout(G, k=100*1/np.sqrt(len(G.nodes())), iterations=2000, scale=1), scale=1, center=(0, 0))
# graph_renderer = from_networkx(G, pos, scale=1)

# graph_renderer.node_renderer.glyph = Circle(size=15, fill_color=Spectral4[0])
# # graph_renderer.edge_renderer.glyph = MultiLine(
# #     line_color="edge_color", line_alpha=0.8, line_width=1)
# plot.renderers.append(graph_renderer)

# this function sets the color of the nodes, but how to set based on the name of the node?
r_circles = plot.circle('x', 'y', source=nodes_source,
                        size=15, color='skyblue', level='overlay')

labels = LabelSet(x='x', y='y', text='name', x_offset=5,
                  y_offset=10, source=nodes_source, render_mode='canvas', text_font_size='8pt', text_baseline='middle')
def get_edges_specs(_network, _layout):
    # d = dict(xs=[], ys=[], alphas=[])
    d = dict(xs=[], ys=[], x0=[], x1=[], y0=[], y1=[], cx0=[],cy0=[],cx1=[],cy1=[])
    # weights = [d['weight'] for u, v, d in _network.edges(data=True)]
    # max_weight = max(weights)

    # def calc_alpha(h): return 0.1 + 0.6 * (h / max_weight)

    # example: { ..., ('user47', 'da_bjoerni', {'weight': 3}), ... }
    for u, v, data in _network.edges(data=True):       

        # nodes1 = np.asfortranarray([x1,y1])
        # curve1 = bezier.Curve(nodes1, degree=2)
        # print(nodes1, curve1)
        d['xs'].append([_layout[u][0], _layout[v][0]])
        d['ys'].append([_layout[u][1], _layout[v][1]])
        # d['alphas'].append(calc_alpha(data['weight']))
        d['x0'].append(_layout[u][0])
        d['y0'] .append(_layout[u][1])
        d['x1'] .append(_layout[v][0])
        d['y1'] .append(_layout[v][1])
        d['cx0'].append( _layout[u][0]-0.2)
        d['cy0'].append( _layout[u][1]-0.2)
        d['cx1'].append( _layout[v][0]+0.2)
        d['cy1'].append( _layout[v][1]+0.2)
        
    return d


lines_source = ColumnDataSource(get_edges_specs(G, pos))

glyph = Bezier(x0='x0', y0='y0', x1='x1', y1='y1', cx0='cx0', cy0='cy0',
               cx1='cx1', cy1='cy1', line_color="#d95f02", line_width=.5)
plot.add_glyph(lines_source, glyph)
# print(get_edges_specs(G, pos))
# r_lines = plot.multi_line('xs', 'ys', line_width=.5,
#                           color='grey',source=lines_source)  # This function sets the color of the edges
plot.add_layout(labels)
output_file("interactive_graphs.html")
show(plot)
# write_dot(G, 'multi.dot')
