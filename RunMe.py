import json
import pandas as pd
import networkx as nx
import numpy as np
from bokeh.plotting import curdoc, figure, gmap
from bokeh.layouts import widgetbox, row, column, Spacer
from bokeh.models import ColumnDataSource, GraphRenderer, GMapOptions, Circle, MultiLine, StaticLayoutProvider, TapTool, HoverTool, Legend, LabelSet
from bokeh.models.widgets import RadioGroup, RadioButtonGroup, Paragraph, Select, Slider
from bokeh.models.graphs import NodesAndLinkedEdges, EdgesAndLinkedNodes
from bokeh.palettes import YlOrRd
from bokeh.transform import dodge
from bokeh.core.properties import value
from bokeh.models.callbacks import CustomJS


# Reading the user network
G = nx.read_gml("user.gml")

# Preprocessing and cleaning businesses file

df = pd.read_csv("nevada_business.csv")
df.drop(columns=['hours.Monday', 'hours.Tuesday', 'hours.Wednesday', 'hours.Thursday', 'hours.Friday', 'hours.Saturday',
                 'hours.Sunday', 'time', 'BusinessAcceptsBitcoin', 'CoatCheck', 'DogsAllowed', 'city', 'postal_code', 'address', 'attributes'],
                 inplace=True)

# Converting checkin time text data to dictonary
s = df['checkins'].tolist()
dictonary = []
for t in s:
    json_acceptable_string = t.replace("'", "\"")
    d = json.loads(json_acceptable_string)
    dictonary.append(d)
df['checkins'] = pd.DataFrame({'col': dictonary})

# Converting ambience time text data to dictonary
s = df['Ambience'].tolist()
dictonary = []
for t in s:
    try:
        t = t.replace("True", "'True'")
        t = t.replace("False", "'False'")
    except:
        t = "{'romantic': 'False', 'intimate': 'False', 'classy': 'False', 'hipster': 'False', 'divey': 'False', 'touristy': 'False', 'trendy': 'False', 'upscale': 'False', 'casual': 'True'}"
    json_acceptable_string = t.replace("'", "\"")
    d = json.loads(json_acceptable_string)
    dictonary.append(d)
df['Ambience'] = pd.DataFrame({'col': dictonary})
doubled_stars = []
for x in df['stars']:
    y = x * 2
    doubled_stars.append(y)
df['stars'] = doubled_stars

# SETTING DEFAULTS FOR SELECTION FLAGS
default_flag = []
l = len(df['business_id'])
for i in range(1, l):
    default_flag.append(int(1))
df['flag_1'] = pd.DataFrame({'col': default_flag})
df['flag_2'] = pd.DataFrame({'col': default_flag})
df['flag_3'] = pd.DataFrame({'col': default_flag})
df['flag_4'] = pd.DataFrame({'col': default_flag})
df['flag_5'] = pd.DataFrame({'col': default_flag})


# FNs TO READ THE WIDGET VALUES AND CONVERT THEM INTO VALID INPUTS FOR THE CHECKIN_AT_HOUR FN

def mapping_day(radio_active_val):
    if (radio_active_val == 0):
        day = 'Mon-'
    elif (radio_active_val == 1):
        day = 'Tue-'
    elif (radio_active_val == 2):
        day = 'Wed-'
    elif (radio_active_val == 3):
        day = 'Thu-'
    elif (radio_active_val == 4):
        day = 'Fri-'
    elif (radio_active_val == 5):
        day = 'Sat-'
    else:
        day = 'Sun-'
    return day


def mapping_hour(slider_val):
    if (slider_val == 0):
        hr = '00'
    elif (slider_val == 1):
        hr = '01'
    elif (slider_val == 2):
        hr = '02'
    elif (slider_val == 3):
        hr = '03'
    elif (slider_val == 4):
        hr = '04'
    elif (slider_val == 5):
        hr = '05'
    elif (slider_val == 6):
        hr = '06'
    elif (slider_val == 7):
        hr = '07'
    elif (slider_val == 8):
        hr = '08'
    elif (slider_val == 9):
        hr = '09'
    elif (slider_val == 10):
        hr = str(slider_val)
    elif (slider_val == 11):
        hr = str(slider_val)
    elif (slider_val == 12):
        hr = str(slider_val)
    elif (slider_val == 13):
        hr = str(slider_val)
    elif (slider_val == 14):
        hr = str(slider_val)
    elif (slider_val == 15):
        hr = str(slider_val)
    elif (slider_val == 16):
        hr = str(slider_val)
    elif (slider_val == 17):
        hr = str(slider_val)
    elif (slider_val == 18):
        hr = str(slider_val)
    elif (slider_val == 19):
        hr = str(slider_val)
    elif (slider_val == 20):
        hr = str(slider_val)
    elif (slider_val == 21):
        hr = str(slider_val)
    elif (slider_val == 22):
        hr = str(slider_val)
    elif (slider_val == 23):
        hr = str(slider_val)
    return hr


# FN TO RETRIEVE CHECKIN COUNTS AT THE SELECTED HOUR
def checkin_at_hour(day, hour):
    disp = []
    l = len(df['checkins'])
    for i in range(0, l):
        try:
            s = df['checkins'][i][day][hour]
            disp.append(s)
        except:
            s = 0
            disp.append(s)
    return disp


def average_checkins(day):
    disp = []
    d = day
    for val in range(0, 24):
        h = mapping_hour(val)
        counts = checkin_at_hour(d, h)
        avg = round(np.mean(counts))
        disp.append(avg)
    return disp


# Create a Selection Function
def selection_avg_checkins(day, flag_5):
    disp = []
    d = day
    f_5 = flag_5
    l = len(df['checkins'])
    for val in range(0, 24):
        counts = []
        h = mapping_hour(val)
        all_counts = checkin_at_hour(d, h)
        i = 0
        for x in all_counts:
            if (f_5[i] == 1):
                s = all_counts[i]
                counts.append(s)
            i += 1
        avg = round(np.mean(counts))
        disp.append(avg)
    return disp


# Simple Neighborhood Selection
def selection_1(neighborhood):
    s1 = neighborhood
    disp = []
    l = len(df['neighborhood'])
    for i in range(0, l):
        try:
            if (df['neighborhood'][i] == s1):
                s = 1
                disp.append(s)
            else:
                if (s1 == 'All'):
                    s = 1
                    disp.append(s)
                else:
                    s = 0
                    disp.append(s)
        except:
            s = 0
            disp.append(s)
    return disp

# Simple Ambience Selection
def selection_2(ambience):
    s2 = ambience
    disp = []
    l = len(df['Ambience'])
    for i in range(0, l):
        try:
            if (df['Ambience'][i][s2] == 'True'):
                s = 1
                disp.append(s)
            else:
                if (s2 == 'All'):
                    s = 1
                    disp.append(s)
                else:
                    s = 0
                    disp.append(s)
        except:
            s = 1
            disp.append(s)
    return disp

# Alcohol type selection
def selection_3(alcohol):
    s3 = alcohol
    disp = []
    l = len(df['Alcohol'])
    for i in range(0, l):
        try:
            if (df['Alcohol'][i] == s3):
                s = 1
                disp.append(s)
            else:
                if (s3 == 'All'):
                    s = 1
                    disp.append(s)
                else:
                    s = 0
                    disp.append(s)
        except:
            s = 0
            disp.append(s)
    return disp

# Establishment Type
def selection_4(category):
    s4 = category
    disp = []
    if (s4 == 'Casinos'):
        disp = df["Casinos"]
    elif (s4 == 'Buffets'):
        disp = df["Buffets"]
    elif (s4 == 'Nightlife'):
        disp = df["Nightlife"]
    elif (s4 == 'Cafes'):
        disp = df["Cafes"]
    else:
        for x in df["categories"]:
            disp.append(1)
    return disp


def agg_selection(flag_1, flag_2, flag_3, flag_4):
    disp = []
    l = len(flag_1)
    for i in range(0, l):
        a = flag_1[i]
        b = flag_2[i]
        c = flag_3[i]
        d = flag_4[i]
        if a == b == c == d == 1:
            s = 1
            disp.append(s)
        else:
            s = 0
            disp.append(s)
    return disp


# Function to assign size based on manual observation of checkin bins
def sizes(checking_at_hour, z):
    checkin = checking_at_hour
    sz = []
    for i in checkin:
        if (0 <= i < 2):
            sz.append(0)
        elif (2 <= i < 10):
            sz.append(.35)
        elif (10 <= i < 20):
            sz.append(0.8)
        elif (20 <= i < 50):
            sz.append(3)
        elif (50 <= i < 100):
            sz.append(4)
        elif (100 <= i < 200):
            sz.append(6)
        elif (200 <= i < 400):
            sz.append(8)
        elif (400 <= i):
            sz.append(10)
    scale_factor = 1
    other_factor = 1
    if z > 11:
        change = (z - 11) * 2
        scale_factor += change
        print("Scale Factor:", scale_factor)
    elif (z == 11):
        scale_factor = 0
        other_factor = 0.8
    else:
        other_factor = 0.6
    sz = [(j * other_factor) + scale_factor for j in sz]
    c = 0
    for x in sz:
        if (x == scale_factor):
            sz[c] = 0
        c += 1
    return sz


# Function to assign color based on manual observation of checkin bins
def colors(flag_5):
    Color_Palette = YlOrRd[8]
    f_5 = flag_5
    clr = []
    for i in f_5:
        if (i == 0):
            clr.append(Color_Palette[4])
        else:
            clr.append(Color_Palette[1])
    return clr


def alpha(flag_5):
    f_5 = flag_5
    alp = []
    for i in f_5:
        if (i == 0):
            alp.append(0.5)
        else:
            alp.append(0.8)
    return alp


# Creating the ColumnDataSource for nodes of the graph
def nodes_df(gr, col):
    node_data = dict(index=[], Col=[], size=[], rate=[])
    for u in gr.nodes():
        node_data['index'].append(u)
        node_data['Col'].append(gr.node[u][col])
        node_data['size'].append(gr.node[u]['size'])
        # node_data['rate'].append(gr.node[u]['rate'])
        node_data['rate'].append([1,2,3,4])
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


# -----------------------------------------------------------------------------------------------------------
# Drawing the different plots
# Creating the Map
def create_map():
    z = zoom.value
    lt = lat.value
    lg = lon.value
    day = mapping_day(days_options.active)
    hour = mapping_hour(slider.value)
    df['checkin_at_hour'] = checkin_at_hour(day, hour)  # adds column df['checkin_at_hour'] for use in size calculation

    sz = sizes(df['checkin_at_hour'], z)
    df['flag_1'] = selection_1(neighborhood.value)
    df['flag_2'] = selection_2(ambience.value)
    df['flag_3'] = selection_3(alcohol.value)
    df['flag_4'] = selection_4(category.value)
    df['flag_5'] = agg_selection(df['flag_1'], df['flag_2'], df['flag_3'], df['flag_4'])
    clr = colors(df['flag_5'])
    alp = alpha(df['flag_5'])

    map_options = GMapOptions(lat=lt, lng=lg, map_type="roadmap", zoom=z)
    bus_hover = HoverTool(
        tooltips=[('Business Name', '@name'), ('Reviews', '@review_count'), ('Checkins', '@checkin_at_hr')],
        names=["bus_hover"])

    p = gmap("AIzaSyAQBImT1FpLK1aQvKq1e-Cfs1xd_NzC0mY", map_options, title="Vegas businesses", plot_width=550, plot_height=550,
             tools=[bus_hover, 'reset', 'pan', 'lasso_select'], toolbar_location="above")

    source = ColumnDataSource(data=dict(lat=df['latitude'], lon=df['longitude'], size=sz, color=clr, alpha=alp,
                                        name=df['name'], review_count=df['review_count'],
                                        checkin_at_hr=df['checkin_at_hour']))

    p.circle(x="lon", y="lat", size="size", fill_alpha="alpha", fill_color="color", name="bus_hover", line_width=1,
             line_alpha=0, hover_alpha=1.0, source=source)
    p.outline_line_alpha = 0
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.xaxis.visible = False
    p.yaxis.visible = False

    return p


# Creating the check in chart
def create_chart():
    Color_Palette = YlOrRd[8]
    hour = list(range(0, 24))
    hour_str = []
    for x in hour:
        hour_str.append(str(x)+":00")

    avg_type = ['Overall', 'Selection']
    day = mapping_day(days_options.active)
    overall = average_checkins(day)
    selection = selection_avg_checkins(day, df['flag_5'])

    hour_str.reverse()
    overall.reverse()
    selection.reverse()
    data = {'hour': hour_str,
            'Overall': overall, 'Selection': selection}

    source = ColumnDataSource(data=data)

    b = figure(y_range=hour_str, x_range=(0, 62), title="Checkin Counts Comparison", y_axis_label='Hour of Day',
               x_axis_label="Average Checkins", toolbar_location=None, tools="", plot_width=290, plot_height=550)
    b.hbar(y=dodge('hour', -0.22, range=b.y_range), right='Overall', height=0.35, source=source,
           color=Color_Palette[4], legend=value("Overall"))

    b.hbar(y=dodge('hour', +0.22, range=b.y_range), right='Selection', height=0.35, source=source, color=Color_Palette[1],
           legend=value("Selection"))

    b.outline_line_alpha = 0
    b.legend.location = "center_right"
    b.legend.orientation = "vertical"
    b.yaxis.axis_line_color = None
    b.yaxis.major_tick_line_color = None
    b.yaxis.major_tick_out = 0
    b.ygrid.grid_line_color = None
    b.xaxis.axis_line_color = None
    b.xaxis.minor_tick_line_color = None
    b.xaxis.major_tick_line_color = "#a7a7a7"

    return b


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
    graph.edge_renderer.glyph = MultiLine(line_alpha='alpha', line_width=0.1, line_color="#d8b7a4")
    graph_layout = dict(nx.get_node_attributes(G, lay))
    graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

    # Glyph properties on selection
    graph.selection_policy = NodesAndLinkedEdges()
    graph.inspection_policy = EdgesAndLinkedNodes()
    graph.node_renderer.selection_glyph = Circle(size=12, fill_color='#0A5EB6', line_color="#002217")
    graph.edge_renderer.selection_glyph = MultiLine(line_color="#2972BE", line_width=0.5, line_alpha=0.4)


    # Adding graph to plot
    plot = figure(title="Yelp Users Layout", x_range=(-6.5, 6.5), y_range=(-6.5, 6.5), plot_width=525, plot_height=525,
                  toolbar_location="above")
    plot.outline_line_alpha = 0
    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = None
    plot.xaxis.visible = False
    plot.yaxis.visible = False
    plot.renderers.append(graph) # Adding graph

    return row(plot)


# ----------------------------------------------------------------------------------------------------------
# Update callback for all changes of the widgets


def update1(attr, old, new):
    layout.children[0].children[0] = create_map()
    layout.children[0].children[1] = create_chart()


def update2(attr, old, new):
    layout.children[0].children[3] = create_graph()


# ----------------------------------------------------------------------------------------------------------
# Dashboard Building

# Position Control
zoom = Slider(start=10, end=15, value=11, step=1, title="Zoom")
zoom.on_change('value', update1)
lat = Slider(start=36, end=36.24, value=36.1200, step=.02, title="Lat Position")
lat.on_change('value', update1)
lon = Slider(start=-115.30, end=-115.06, value=-115.18, step=.02, title="Lon Position")
lon.on_change('value', update1)

# Time Control
days_options = RadioButtonGroup(labels=["M", "T", "W", "T", "F", "S", "S"], active=5)
days_options.on_change('active', update1)

slider = Slider(start=0, end=23, value=0, step=1, title="Hour of Day")
slider.on_change('value', update1)

# Select Options
neighborhood_options = list(set(df['neighborhood']))[1:]
alcohol_options = ['beer_and_wine', 'full_bar', 'none']
ambience = df['Ambience'][0]
ambience_options = [*ambience]
category_options = ['Casinos', 'Buffets', 'Nightlife', 'Cafes']

# Select Widgets
neighborhood = Select(title='Neighborhood', value='All', options=['All'] + neighborhood_options)
neighborhood.on_change('value', update1)
ambience = Select(title='Ambience', value='All', options=['All'] + ambience_options)
ambience.on_change('value', update1)
alcohol = Select(title='Alcohol', value='All', options=['All'] + alcohol_options)
alcohol.on_change('value', update1)
category = Select(title='Establishment Type', value='All', options=['All'] + category_options)
category.on_change('value', update1)


# Radio buttons for changing layouts and colors
radio_layout = RadioGroup(
        labels=["Degree", "Betweenness", "Communicability"], active=0)
radio_layout.on_change('active', update2)

radio_color = RadioGroup(
        labels=["Degree", "Betweenness", "Friends", "Reviews", "Compliments"], active=1)
radio_color.on_change('active', update2)

t1 = Paragraph(text="""User Layout""")
t2 = Paragraph(text="""User Color Scheme""")

# Arrangement

# user_control = widgetbox([t1, radio_layout, t2, radio_color], width=170)
# time_control = widgetbox([days_options, slider], width=270)
# position_control = widgetbox([zoom, lat, lon], width=140)
# select_box = widgetbox(neighborhood, ambience, alcohol, category, width=150)

user_control = row(widgetbox([t1, radio_layout], width=170), widgetbox([t2, radio_color], width=170))
time_control = row(widgetbox([Paragraph(text="""Day of Week"""),days_options], width=270), widgetbox(slider, width=270))
position_control = row(widgetbox(zoom, width=170), widgetbox(lat, width=180), widgetbox(lon, width=180))
select_box = row(widgetbox(neighborhood, ambience, width=150), widgetbox(category, alcohol, width=150))

# layout = column(row(create_map(),
#                     Spacer(width=20),
#                     column(position_control, time_control, Spacer(height=50), row(Spacer(width=130), user_control)),
#                     create_graph()),
#                 row(create_chart(), select_box))


layout = column(row(create_map(),create_chart(),Spacer(width=20),create_graph()),
                row(column(position_control, Spacer(height=10), time_control), Spacer(width=30), select_box, Spacer(width=20), user_control))#, create_dummy_legend()))

curdoc().add_root(layout)
curdoc().title = "Vegas Yelp - Businesses & Users"
