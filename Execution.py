import networkx as nx
import numpy as np
from bokeh.plotting import curdoc, figure
from bokeh.layouts import widgetbox, row, gridplot
from bokeh.models import GraphRenderer, Circle, MultiLine, StaticLayoutProvider, TapTool, CustomJS
from bokeh.models.widgets import RadioButtonGroup
from bokeh.models.graphs import NodesAndLinkedEdges, EdgesAndLinkedNodes


G = nx.read_gml("user.gml")

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


def nodes_df(gr, col):
    node_data = dict(index=[], Col=[])
    for u in gr.nodes():
        node_data['index'].append(u)
        node_data['Col'].append(gr.node[u][col])
    return node_data


def edges_df(gr):
    edges_data = dict(start=[], end=[], alpha=[])
    maxw = 50
    for u, v, d in gr.edges(data=True):
        edges_data['start'].append(u)
        edges_data['end'].append(v)
        edges_data['alpha'].append(min(1,(d['strength']/maxw)))
    return edges_data


def create_figure():
    if radio_layout.active == 0:
        lay = 'WDegreepos'
    elif radio_layout.active == 1:
        lay = 'bwcentralpos'
    else:
        lay = 'ccentralpos'

    if radio_color.active == 0:
        col = 'DegCol'
    elif radio_layout.active == 1:
        col = 'Colbw'
    else:
        col = 'Colcc'

    # Create adjacency matrix view
    matp = figure(title="Adjacency Matrix", x_range=allnodes, y_range=allnodes)
    matp.rect(allnodes * numnodes, np.repeat(allnodes, numnodes), color=adjcol, width=1, height=1)
    matp.xgrid.grid_line_color = None
    matp.ygrid.grid_line_color = None
    matp.xaxis.visible = False
    matp.yaxis.visible = False

    # Create Network view
    graph = GraphRenderer()
    graph.node_renderer.data_source.data = nodes_df(G, col)
    graph.edge_renderer.data_source.data = edges_df(G)
    graph.node_renderer.glyph = Circle(size=3, fill_color='Col', line_color=None, line_alpha=0.1, fill_alpha=1)
    graph.edge_renderer.glyph = MultiLine(line_alpha='alpha', line_width=0.1, line_color="#A0DF3F")
    graph_layout = dict(nx.get_node_attributes(G, lay))
    graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

    # Glyph properties on selection
    graph.selection_policy = NodesAndLinkedEdges()
    graph.inspection_policy = EdgesAndLinkedNodes()
    graph.node_renderer.selection_glyph = Circle(size=12, fill_color='red')
    graph.edge_renderer.selection_glyph = MultiLine(line_color='black', line_width=0.5, line_alpha=0.8)

    # Callback for Taptool
    # callback = CustomJS(args=dict(source=graph.node_renderer.data_source), code="""
    #    console.log(cb_data)
    #    var inds = cb_data.source.selected['1d'].indices;
    #    window.alert(inds);
    #    """)

    # Adding graph to plot
    plot = figure(title="Graph Layout Demonstration", x_range=(-6.5, 6.5), y_range=(-6.5, 6.5))
    plot.outline_line_alpha = 0
    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = None
    plot.xaxis.visible = False
    plot.yaxis.visible = False
    plot.renderers.append(graph)
    plot.add_tools(TapTool())

    gplot = gridplot([matp, plot], ncols=2)
    return gplot


def update(attr, old, new):
    print(attr, old, new)
    layout.children[1] = create_figure()


#Radio buttons for changing layouts and colors
radio_layout = RadioButtonGroup(
        labels=["Degree", "Betweenness", "Communicability"], active=0)
radio_layout.on_change('active', update)

radio_color = RadioButtonGroup(
        labels=["Degree", "Betweenness", "Communicability"], active=1)
radio_color.on_change('active', update)

widget = widgetbox([radio_layout, radio_color], width=300)
layout = row(create_figure(), widget)

curdoc().add_root(layout)
