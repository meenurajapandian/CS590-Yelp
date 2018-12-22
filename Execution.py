import networkx as nx
from bokeh.plotting import curdoc, figure
from bokeh.layouts import widgetbox, row
from bokeh.models import GraphRenderer, Circle, MultiLine, StaticLayoutProvider, TapTool
from bokeh.models.widgets import RadioGroup, Paragraph
from bokeh.models.graphs import NodesAndLinkedEdges, EdgesAndLinkedNodes


# Reading the user network
G = nx.read_gml("user.gml")

# Creating the ColumnDataSource for nodes of the graph
def nodes_df(gr, col):
    node_data = dict(index=[], Col=[], size=[])
    for u in gr.nodes():
        node_data['index'].append(u)
        node_data['Col'].append(gr.node[u][col])
        node_data['size'].append(gr.node[u]['size'])
    return node_data

# Creating the ColumnDataSource for edges of the graph
def edges_df(gr):
    edges_data = dict(start=[], end=[], alpha=[])
    maxw = 30
    for u, v, d in gr.edges(data=True):
        edges_data['start'].append(u)
        edges_data['end'].append(v)
        edges_data['alpha'].append(min(1,(d['strength']/maxw)))
    return edges_data


# Creating the network visualization
def create_graph():
    #Find the layout and color choice
    if radio_layout.active == 0:
        lay = 'WDegreepos'
    elif radio_layout.active == 1:
        lay = 'bwcentralpos'
    else:
        lay = 'ccentralpos'

    if radio_color.active == 0:
        col = 'DegCol'
    elif radio_color.active == 1:
        col = 'Colbw'
    elif radio_color.active == 2:
        col = 'friend'
    elif radio_color.active == 3:
        col = 'reviewcount'
    else:
        col = 'comprank'


    # Create Network view
    graph = GraphRenderer()
    graph.node_renderer.data_source.data = nodes_df(G, col)
    graph.edge_renderer.data_source.data = edges_df(G)
    graph.node_renderer.glyph = Circle(size='size', fill_color='Col', line_color="black", line_alpha = 0.1, fill_alpha=1)
    graph.edge_renderer.glyph = MultiLine(line_alpha='alpha', line_width=0.1, line_color="#A0DF3F")
    graph_layout = dict(nx.get_node_attributes(G, lay))
    graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

    # Glyph properties on selection
    graph.selection_policy = NodesAndLinkedEdges()
    graph.inspection_policy = EdgesAndLinkedNodes()
    graph.node_renderer.selection_glyph = Circle(size=12, fill_color='#0A5EB6', line_color="#002217")
    graph.edge_renderer.selection_glyph = MultiLine(line_color="#2972BE", line_width=0.5, line_alpha=0.4)


    # Adding graph to plot
    plot = figure(title="Yelp Users Layout", x_range=(-6.5, 6.5), y_range=(-6.5, 6.5))
    plot.outline_line_alpha = 0
    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = None
    plot.xaxis.visible = False
    plot.yaxis.visible = False
    plot.renderers.append(graph)
    plot.add_tools(TapTool())

    return plot


def update(attr, old, new):
    print(attr, old, new)
    layout.children[0] = create_graph()


#Radio buttons for changing layouts and colors
radio_layout = RadioGroup(
        labels=["Degree", "Betweenness", "Communicability"], active=0)
radio_layout.on_change('active', update)

radio_color = RadioGroup(
        labels=["Degree", "Betweenness", "Friends", "Reviews", "Compliments"], active=1)
radio_color.on_change('active', update)

t1 = Paragraph(text="""Layout""")
t2 = Paragraph(text="""Color Scheme""")

widget = widgetbox([t1, radio_layout, t2, radio_color], width=300)
layout = row(create_graph(), widget)

curdoc().add_root(layout)
