import pandas as pd
import networkx as nx
import numpy as np
from bokeh.models.widgets import Slider
from bokeh.layouts import row, widgetbox
from bokeh.plotting import figure, curdoc
from bokeh.models import CustomJS, MultiLine, StaticLayoutProvider, TapTool, ColumnDataSource, HoverTool, LogColorMapper, CategoricalColorMapper, GraphRenderer, Circle
from bokeh.models.graphs import from_networkx, NodesAndLinkedEdges, EdgesAndLinkedNodes
from bokeh.io import show, output_file


df = pd.read_csv('C:/Users/Meenu/PycharmProjects/CS590/CS590-Yelp/usernetwork.csv')
df['distance'] = 1/df['strength']
df_user = pd.read_csv('C:/Users/Meenu/PycharmProjects/CS590/CS590-Yelp/userdetails.csv')
del df_user['Unnamed: 0']

G = nx.from_pandas_edgelist(df, 'user1', 'user2', ['strength','distance'])
print(G.number_of_nodes())
#nx.set_node_attributes(G, nx.betweenness_centrality(G, weight='distance'), 'bwcentral')
#nx.set_node_attributes(G, dict(nx.betweenness_centrality(G, weight='distance', 'bwcentral')))
nx.set_node_attributes(G, df_user.set_index('user_id').to_dict('index'))
nx.set_node_attributes(G, dict(G.degree(weight='strength')), 'WDegree')
values = np.percentile(list(nx.get_node_attributes(G,'WDegree').values()), [100, 95, 85, 70, 40])
values = np.append(values, 0)
#values = np.percentile(list(nx.get_node_attributes(G,'bwcentral').values()), [100, 95, 85, 70, 40])
#values = np.append(values, 0)
nodep = []
nodex = []
nodey = []

for i in range(0,5):
    nodes = list(set(u for u in G.nodes()
                if G.node[u]['WDegree'] >= values[i+1] and G.node[u]['WDegree'] < values[i]))
    #for j in range(0,len(nodes)):
    nodep.extend(nodes)
    #s, t = np.random.multivariate_normal(mean, cov, len(nodes)).T
    s = np.random.normal(0, 0.9, len(nodes))
    #s = [x+i if x > 0 else x-i for x in s]
    t = np.random.normal(0, 0.9, len(nodes))
    #t = [x+i if x > 0 else x-i for x in t]
    h = [np.sqrt((x**2)+(y**2)) for x,y in zip(s,t)]
    s = [x * (1 + (i / z)) for x, z in zip(s, h)]
    t = [x * (1 + (i / z)) for x, z in zip(t, h)]
    nodex.extend(s)
    nodey.extend(t)
    #t = np.linspace(0,1,len(nodes)+1)[:-1]*2*np.pi
    #nodex.extend(np.cos(t)*(i+1))
    #nodey.extend(np.sin(t)*(i+1))


def nodes_df(gr):
    node_data = dict(index=[], DegCol=[], businesses=[], reviewcount=[], friend=[], comprank=[], name=[],
                    yelpingsince=[])
    for u in gr.nodes():
        node_data['index'].append(u)
        node_data['businesses'].append(gr.node[u]['businesses'])
        node_data['reviewcount'].append(gr.node[u]['reviewcount'])
        node_data['friend'].append(gr.node[u]['friend'])
        node_data['comprank'].append(gr.node[u]['comprank'])
        node_data['name'].append(gr.node[u]['name'])
        node_data['yelpingsince'].append(gr.node[u]['yelpingsince'])
        if gr.node[u]['WDegree'] < 900:
            node_data['DegCol'].append('#FFAAAA')
        elif gr.node[u]['WDegree'] < 1413:
            node_data['DegCol'].append('#D46A6A')
        elif gr.node[u]['WDegree'] < 1885:
            node_data['DegCol'].append('#AA3939')
        elif gr.node[u]['WDegree'] < 2743:
            node_data['DegCol'].append('#801515')
        else:
            node_data['DegCol'].append('#550000')
    return node_data


def edges_df(gr):
    edges_data = dict(start=[], end=[], alpha=[])
    #maxw = max(dict(gr.edges).items(), key=lambda x:x[1]['strength'])[1]['strength']
    maxw = 40
    for u, v, d in gr.edges(data=True):
        edges_data['start'].append(u)
        edges_data['end'].append(v)
        edges_data['alpha'].append(min(1,(d['strength']/maxw)))
    return edges_data


#def layout(gr):
#nx.set_node_attributes(G, Degree_color, "degree_color")
plot = figure(title="Graph Layout Demonstration", x_range=(-5.1,5.1), y_range=(-5.1,5.1))
allnodes = list(G.nodes())
numnodes = len(allnodes)
adj = np.array(nx.to_numpy_matrix(G)).flatten().tolist()

adjval = np.percentile(adj, [20, 50, 75, 88, 95])
adjcol = []
for i in range(len(adj)):
    if adj[i] < adjval[0]:
        adjcol.append('#FDF5CA')
    elif adj[i] < adjval[1]:
        adjcol.append('#FDF2B1')
    elif adj[i] < adjval[2]:
        adjcol.append('#FDEE98')
    elif adj[i] < adjval[3]:
        adjcol.append('#FDE665')
    elif adj[i] < adjval[4]:
        adjcol.append('#FDDF33')
    else:
        adjcol.append('#FDD700')


#mapper = LogColorMapper(palette=['#FDFDFD', '#FDF5CA', '#FDF2B1', '#FDEE98', '#FDE665', '#FDDF33', '#FDD700'],
#                            low=min(adj), high=max(adj))

# check order of ad
matp = figure(title="Adjacency Matrix", x_range=allnodes, y_range=allnodes)
matp.rect(allnodes*numnodes, np.repeat(allnodes,numnodes), color=adjcol, width=1, height=1)
matp.xaxis.major_label_text_font_size = '0pt'  # turn off x-axis tick labels
matp.yaxis.major_label_text_font_size = '0pt'

graph = GraphRenderer()
graph.node_renderer.data_source.data = nodes_df(G)
graph.edge_renderer.data_source.data = edges_df(G)
graph.node_renderer.glyph = Circle(size=3, fill_color='DegCol', line_color=None, line_alpha=0.1, fill_alpha = 1)
graph.node_renderer.selection_glyph = Circle(size=10, fill_color = 'red')
graph.edge_renderer.glyph = MultiLine(line_alpha='alpha', line_width=0.1, line_color="grey")
graph.edge_renderer.selection_glyph = MultiLine(line_color='black', line_width=0.5, line_alpha=0.8)

#graph_layout = layout(G)
graph_layout = dict(zip(nodep, zip(nodex, nodey)))
#graph_layout = nx.spring_layout(G, weight='distance')
graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)


# def bezier(start, end, control, steps):
#     return[(1-s)**2*start + s*(1-s)*s*control + s**2*end for s in steps]
#
#
# xs, ys = [], []
# sx, sy = graph_layout[0]
# steps = [i/100 for i in range(100)]
# for node_index in G.nodes():
#     ex, ey = graph_layout[node_index]
#     xs.append(bezier(sx, ex, 0, steps))
#     ys.append(bezier(sy, ey, 0, steps))
#
# graph.edge_renderer.data_source.data['xs'] = xs
# graph.edge_renderer.data_source.data['ys'] = ys

#Hover Properties
node_hover_tool = HoverTool(tooltips=[("Name", "@name"),
                                      ("Yelper Since", "@yelpingsince"),
                                      ("Total Reviews", "@reviewcount"),
                                      ("Average stars", "@averagestars"),
                                      ("Friends", "@friend"),
                                      ("Fans", "@fans"),
                                      ("Compliment Ranking", "@comprank")])


callback = CustomJS(args = dict(source = graph.node_renderer.data_source), code =
    """
    console.log(cb_data)
    var inds = cb_data.source.selected['1d'].indices;
    window.alert(inds);
    """)

plot.add_tools(node_hover_tool, callback=callback)

graph.selection_policy = NodesAndLinkedEdges()
graph.inspection_policy = EdgesAndLinkedNodes()

plot.renderers.append(graph)
plot.add_tools(TapTool())
#output_file("networkx_graph.html")

#show(plot)
def handler(attr, old, new):
    print('attr: {} old: {} new: {}'.format(attr, old, new))

graph.node_renderer.data_source.on_change('selected', handler)


curdoc().add_root(plot)

