import pandas as pd
import networkx as nx
import numpy as np
import copy

from bokeh.models.widgets import Slider
from bokeh.layouts import row, widgetbox
from bokeh.plotting import figure, curdoc
from bokeh.models import MultiLine, StaticLayoutProvider, TapTool, ColumnDataSource, HoverTool, LogColorMapper, CategoricalColorMapper, GraphRenderer, Circle
from bokeh.palettes import Category20, Category20b, Category20c
from bokeh.models.graphs import from_networkx, NodesAndLinkedEdges, EdgesAndLinkedNodes
from bokeh.io import show, output_file


df = pd.read_csv('C:/Users/Meenu/PycharmProjects/CS590/CS590-Yelp/usernetwork.csv')
G = nx.from_pandas_edgelist(df, 'user1', 'user2', 'strength')
nx.set_node_attributes(G, dict(G.degree(weight='strength')), 'WDegree')
values = [0, 21, 39, 66, 119, 3700]
nodep = []
nodex = []
nodey = []

for i in range(0,5):
    nodes = list(set(u for u in G.nodes()
                if G.node[u]['WDegree'] < values[i+1] and G.node[u]['WDegree'] > values[i]))
    #for j in range(0,len(nodes)):
    nodep.extend(nodes)
    t = np.linspace(0,1,len(nodes)+1)[:-1]*2*np.pi
    nodex.extend(np.cos(t)*(i+1))
    nodey.extend(np.sin(t)*(i+1))


#for u in G.nodes():
#    if G.node[u]['WDegree'] < 21:
#        G.node[u]['DegCom'] = 5
#    elif G.node[u]['WDegree'] < 39:
#        G.node[u]['DegCom'] = 4
#    elif G.node[u]['WDegree'] < 66:
#        G.node[u]['DegCom'] = 3
#    elif G.node[u]['WDegree'] < 119:
#        G.node[u]['DegCom'] = 2
#    else:
#        G.node[u]['DegCom'] = 1

def nodes_df(gr):
    node_data = dict(index=[], DegCol=[])
    for u in gr.nodes():
        node_data['index'].append(u)
        if gr.node[u]['WDegree'] < 21:
            node_data['DegCol'].append('#FFAAAA')
        elif gr.node[u]['WDegree'] < 39:
            node_data['DegCol'].append('#D46A6A')
        elif gr.node[u]['WDegree'] < 66:
            node_data['DegCol'].append('#AA3939')
        elif gr.node[u]['WDegree'] < 119:
            node_data['DegCol'].append('#801515')
        else:
            node_data['DegCol'].append('#550000')
    return node_data


def edges_df(gr):
    edges_data = dict(start=[], end=[], alpha=[])
    maxw = max(dict(gr.edges).items(), key=lambda x:x[1]['strength'])[1]['strength']
    for u, v, d in gr.edges(data=True):
        edges_data['start'].append(u)
        edges_data['end'].append(v)
        edges_data['alpha'].append(d['strength']/maxw)
    return edges_data


#def layout(gr):



#nx.set_node_attributes(G, Degree_color, "degree_color")
plot = figure(title="Graph Layout Demonstration", x_range=(-1.1,1.1), y_range=(-1.1,1.1))

graph = GraphRenderer()
graph.node_renderer.data_source.data = nodes_df(G)
graph.edge_renderer.data_source.data = edges_df(G)
graph.node_renderer.glyph = Circle(size=15, fill_color='DegCol', line_alpha=0, fill_alpha =0.5)
graph.node_renderer.selection_glyph = Circle(size=17, fill_color = 'red')
graph.edge_renderer.glyph = MultiLine(line_alpha='alpha', line_width=0.1, line_color="grey")
graph.edge_renderer.selection_glyph = MultiLine(line_color='black', line_width=0.5, line_alpha=1)

#graph_layout = layout(G)
graph_layout = dict(zip(nodep, zip(nodex, nodey)))
graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

graph.selection_policy = NodesAndLinkedEdges()

plot.renderers.append(graph)
plot.add_tools(TapTool())
output_file("networkx_graph.html")
show(plot)
