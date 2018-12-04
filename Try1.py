import pandas as pd
import networkx as nx
import numpy as np
from bokeh.models.widgets import Slider
from bokeh.layouts import row, widgetbox
from bokeh.plotting import figure, curdoc
from bokeh.models import MultiLine, StaticLayoutProvider, TapTool, ColumnDataSource, HoverTool, LogColorMapper, CategoricalColorMapper, GraphRenderer, Circle
from bokeh.models.graphs import from_networkx, NodesAndLinkedEdges, EdgesAndLinkedNodes
from bokeh.io import show, output_file


df = pd.read_csv('C:/Users/Meenu/PycharmProjects/CS590/CS590-Yelp/usernetwork.csv')
df['distance'] = 1/df['strength']
df_user = pd.read_csv('C:/Users/Meenu/PycharmProjects/CS590/CS590-Yelp/userdetails.csv')


G = nx.from_pandas_edgelist(df, 'user1', 'user2', ['strength','distance'])
nx.set_node_attributes(G, dict(nx.betweenness_centrality(G, weight='distance'), 'bwcentral'))
#nx.set_node_attributes(G, dict(nx.betweenness_centrality(G, weight='distance', 'bwcentral')))
nx.set_node_attributes(G, df_user.set_index('user_id').to_dict('index'))
nx.set_node_attributes(G, dict(G.degree(weight='strength')), 'WDegree')
values = [3700, 119, 66, 39, 21, 0]
nodep = []
nodex = []
nodey = []

for i in range(0,5):
    nodes = list(set(u for u in G.nodes()
                if G.node[u]['WDegree'] >= values[i+1] and G.node[u]['WDegree'] < values[i]))
    #for j in range(0,len(nodes)):
    nodep.extend(nodes)
    t = np.linspace(0,1,len(nodes)+1)[:-1]*2*np.pi
    nodex.extend(np.cos(t)*(i+1))
    nodey.extend(np.sin(t)*(i+1))


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
    #maxw = max(dict(gr.edges).items(), key=lambda x:x[1]['strength'])[1]['strength']
    maxw = 30
    for u, v, d in gr.edges(data=True):
        edges_data['start'].append(u)
        edges_data['end'].append(v)
        edges_data['alpha'].append(min(1,(d['strength']/maxw)))
    return edges_data


#def layout(gr):
#nx.set_node_attributes(G, Degree_color, "degree_color")
plot = figure(title="Graph Layout Demonstration", x_range=(-5.1,5.1), y_range=(-5.1,5.1))

graph = GraphRenderer()
graph.node_renderer.data_source.data = nodes_df(G)
graph.edge_renderer.data_source.data = edges_df(G)
graph.node_renderer.glyph = Circle(size=15, fill_color='DegCol', line_color='black', line_alpha=0.5, fill_alpha =0.5)
graph.node_renderer.selection_glyph = Circle(size=7, fill_color = 'red')
graph.edge_renderer.glyph = MultiLine(line_alpha='alpha', line_width=0.1, line_color="grey")
graph.edge_renderer.selection_glyph = MultiLine(line_color='black', line_width=0.5, line_alpha=1)

#graph_layout = layout(G)
graph_layout = dict(zip(nodep, zip(nodex, nodey)))
graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

#Hover Properties
node_hover_tool = HoverTool(tooltips=[("Name", "@name"),
                                      ("Yelper Since", "@yelping_since{}"),
                                      ("Total Reviews", "@review_count"),
                                      ("Average stars", "@average_stars"),
                                      ("Friends", "@friends"),
                                      ("Fans", "@fans"),
                                      ("Compliment Ranking", "@comp_tile")])
plot.add_tools(node_hover_tool)

graph.selection_policy = NodesAndLinkedEdges()

plot.renderers.append(graph)
plot.add_tools(TapTool())
output_file("networkx_graph.html")
show(plot)
