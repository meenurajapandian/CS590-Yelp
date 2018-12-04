import pandas as pd
import networkx as nx
import copy

from bokeh.models.widgets import Slider
from bokeh.layouts import row, widgetbox
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, HoverTool, LogColorMapper, CategoricalColorMapper
from bokeh.palettes import Category20, Category20b, Category20c

from bokeh.io import show, output_notebook

df = pd.read_csv('C:/Users/Meenu/PycharmProjects/CS590/CS590-Yelp/usernetwork.csv')
users = nx.from_pandas_edgelist(df, 'user1', 'user2', 'strength')
G1 = users
nx.set_node_attributes(G1, dict(G1.degree(weight='strength')), 'WDegree')

#df_tograph = df_position.set_index('ID').to_dict('index')
#nx.set_node_attributes(G, df_tograph)


def nodes_df(gr):
    node_data = dict(x=[], y=[], Name=[], Degree=[], WDegree=[], size=[], state=[])
    for u in gr.nodes():
        node_data['x'].append(gr.node[u]['lon'])
        node_data['y'].append(gr.node[u]['lat'])
        node_data['state'].append(gr.node[u]['state'])
        node_data['Name'].append(gr.node[u]['name'])
        node_data['Degree'].append(gr.node[u]['Degree'])
        node_data['WDegree'].append(gr.node[u]['WDegree'])
        node_data['size'].append((1.5*gr.node[u]['WDegree']) + 3)
    return node_data


def edges_df(gr):
    edges_data = dict(xs=[], ys=[], city1=[], city2=[], line_width=[], alphas=[], weight=[])
    calc_alpha = lambda h: 0.5 + (h * 0.95)
    calc_width = lambda h: 1.4 + (h * 10)
    for u, v, d in gr.edges(data=True):
        edges_data['xs'].append([gr.node[u]['lon'], gr.node[v]['lon']])
        edges_data['ys'].append([gr.node[u]['lat'], gr.node[v]['lat']])
        edges_data['city1'].append(gr.node[u]['name'])
        edges_data['city2'].append(gr.node[v]['name'])
        edges_data['weight'].append(d['Weight'])
        edges_data['alphas'].append(calc_alpha(d['Weight']))
        edges_data['line_width'].append(calc_width(d['Weight']))
    return edges_data


def create_figure():
    G1 = copy.deepcopy(G)
    nx.set_node_attributes(G1, dict(G1.degree(weight='Weight')), 'WDegree')
    nx.set_node_attributes(G1, dict(G1.degree()), 'Degree')
    rem_edg = []
    for u,v,d in G1.edges(data=True):
        if d['Weight'] < edf.value:
            rem_edg.append((u,v))
    G1.remove_edges_from(rem_edg)
    rem_node = []
    for u in G1.nodes():
        if G1.node[u]['WDegree'] < ndf.value:
            rem_node.append(u)
    rem_node = rem_node+list(nx.isolates(G1))
    G1.remove_nodes_from(rem_node)
    node_df = ColumnDataSource(nodes_df(G1))
    edge_df = ColumnDataSource(edges_df(G1))
    color_mapper = CategoricalColorMapper(factors=states, palette=Category20b[20] + Category20c[20] + Category20[20])
    mapper = LogColorMapper(palette=['#FDFDFD', '#FDF5CA', '#FDF2B1', '#FDEE98', '#FDE665', '#FDDF33', '#FDD700'],
                            low=min(edge_df.data['weight']), high=max(edge_df.data['weight']))

    p = figure(title="US Air Flights in 97", toolbar_location="left", plot_width=1100, plot_height=600,
               match_aspect=True, aspect_scale=0.7, x_range=[-140, -50], y_range=[20, 55])
    r1 = p.circle('x', 'y', source=node_df, size='size', level='overlay',
                  color={'field': 'state', 'transform': color_mapper},
                  alpha=0.8, line_color='#240606', line_width=1, line_alpha=0.3)
    r2 = p.multi_line('xs', 'ys', line_width='line_width', alpha='alphas',
                      color={'field': 'weight', 'transform': mapper},
                      source=edge_df)

    node_hover = HoverTool(tooltips=[('Name', '@Name'), ('State', '@state'), ('No. of Connections', '@Degree'),
                                     ('Total Frequency', '@WDegree')], renderers=[r1])
    node_hover.attachment = 'right'
    edge_hover = HoverTool(tooltips=[('Airports', '@city1'), ('', '@city2'), ('Frequency', '@weight')], renderers=[r2])
    edge_hover.line_policy = 'interp'
    edge_hover.attachment = 'left'
    p.add_tools(node_hover)
    p.add_tools(edge_hover)
    return p


def update(attr, old, new):
    layout.children[1] = create_figure()


ndf = Slider(start=0, end=10, value=0, step=.1, title="Min. Node")
ndf.on_change('value', update)

edf = Slider(start=0, end=0.6, value=0, step=.05, title="Min. Edge Frequency")
edf.on_change('value', update)

controls = widgetbox([ndf, edf], width=300)
layout = row(controls, create_figure())
curdoc().add_root(layout)
