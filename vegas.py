import pandas as pd
import json

from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, GMapOptions, RadioButtonGroup, Slider, Toggle, Select
from bokeh.plotting import gmap, curdoc, figure 
from bokeh.layouts import widgetbox, row, column
from bokeh.palettes import RdBu7 as Color_Palette
from bokeh.transform import dodge
from bokeh.core.properties import value
from statistics import mean

# INITIAL DATAFRAME MANIPULATIONS

df = pd.read_csv("nevada_business_cleaned.csv")
df.drop(columns=['hours.Monday', 'hours.Tuesday','hours.Wednesday', 'hours.Thursday', 'hours.Friday','hours.Saturday','hours.Sunday'
         ,'time','BusinessAcceptsBitcoin','CoatCheck','DogsAllowed','city','postal_code','address', 'attributes'], inplace = True)
#Converting checkin time text data to dictonary
s = df['checkins'].tolist()
dictonary = []
for t in s:
    json_acceptable_string = t.replace("'", "\"")
    d = json.loads(json_acceptable_string)
    dictonary.append(d)
df['checkins'] = pd.DataFrame({'col':dictonary})
#Converting ambience time text data to dictonary
s = df['Ambience'].tolist()
dictonary = []
for t in s:
    try:
        t = t.replace("True","'True'")
        t = t.replace("False","'False'")
    except:
        t = "{'romantic': 'False', 'intimate': 'False', 'classy': 'False', 'hipster': 'False', 'divey': 'False', 'touristy': 'False', 'trendy': 'False', 'upscale': 'False', 'casual': 'True'}"
    json_acceptable_string = t.replace("'", "\"")
    d = json.loads(json_acceptable_string)
    dictonary.append(d)
df['Ambience'] = pd.DataFrame({'col':dictonary})
doubled_stars = []
for x in df['stars']:
    y = x*2
    doubled_stars.append(y)
df['stars'] = doubled_stars
#####SETTING DEFAULTS FOR SELECTION FLAGS
default_flag = []
l = len(df['business_id'])
for i in range(1,l):
    default_flag.append(int(1))
df['flag_1'] = pd.DataFrame({'col':default_flag})
df['flag_2'] = pd.DataFrame({'col':default_flag})
df['flag_3'] = pd.DataFrame({'col':default_flag})
df['flag_4'] = pd.DataFrame({'col':default_flag})
df['flag_5'] = pd.DataFrame({'col':default_flag})

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#FNs TO READ THE WIDGET VALUES AND CONVERT THEM INTO VALID INPUTS FOR THE CHECKIN_AT_HOUR FN

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

#FN TO RETRIEVE CHECKIN COUNTS AT THE SELECTED HOUR 
def checkin_at_hour(day, hour):
    disp = []
    l = len(df['checkins'])
    for i in range(0,l):
        try:
            s = df['checkins'][i][day][hour]
            disp.append(s)
        except:
            print("WE GOT AN EXCEPTION HERE!!")
            s = 0
            disp.append(s)
    return disp

##TESTED
#day = mapping_day(days_options.active)
#hour = mapping_hour(slider.value)
#checkin_at_hour(day, hour)
#df['checkin_at_hour'][0]

def average_checkins(day):
    disp=[]
    d = day
    for val in range(0,24):
        h = mapping_hour(val)
        counts = checkin_at_hour(d,h)
        avg = round(mean(counts))
        disp.append(avg)
    return disp

#Create a Selection Function
#Simple Neighborhood Selection
def selection_1(neighborhood):
    s1 = neighborhood
    disp = []
    l = len(df['neighborhood'])
    for i in range(0,l):
        try:
            if (df['neighborhood'][i]==s1):
                s = 1
                disp.append(s)
            else:
                if (s1=='All'):
                    s = 1
                    disp.append(s)
                else:
                    s = 0
                    disp.append(s)
        except:
            s = 0
            disp.append(s)
    return disp

def selection_2(ambience):
    s2 = ambience
    disp = []
    l = len(df['Ambience'])
    for i in range(0,l):
        try:
            if (df['Ambience'][i][s2]=='True'):
                s = 1
                disp.append(s)
            else:
                if (s2=='All'):
                    s = 1
                    disp.append(s)
                else:
                    s = 0
                    disp.append(s)
        except:
            s = 1
            disp.append(s)
    return disp

def selection_3(alcohol):
    s3 = alcohol
    disp = []
    l = len(df['Alcohol'])
    for i in range(0,l):
        try:
            if (df['Alcohol'][i]==s3):
                s = 1
                disp.append(s)
            else:
                if (s3=='All'):
                    s = 1
                    disp.append(s)
                else:
                    s = 0
                    disp.append(s)
        except:
            s = 0
            disp.append(s)
    return disp

def agg_selection(flag_1,flag_2,flag_3):
    disp = []
    l = len(flag_1)
    for i in range(0,l):
        a = flag_1[i]
        b = flag_2[i]
        c = flag_3[i]
        if a == b == c == 1:
            s = 1
            disp.append(s)
        else:
            s = 0
            disp.append(s)
    return disp      
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Function to assign size based on manual observation of checkin bins
def sizes(checking_at_hour):
    checkin = checking_at_hour
    sz = []
    for i in checkin:
        if (0 <= i < 2):
            sz.append(0)
        elif (2 <= i < 10):
            sz.append(.5)
        elif (10 <= i < 20):
            sz.append(1)
        elif (20 <= i < 50):
            sz.append(3)
        elif (50 <= i < 100):
            sz.append(5)
        elif (100 <= i < 200):
            sz.append(7)
        elif (200 <= i < 400):
            sz.append(9)
        elif (400 <= i):
            sz.append(12)
    return sz

#Function to assign color based on manual observation of checkin bins
def colors(flag_5):
    f_5 = flag_5 
    clr = []
    for i in f_5:
        if (i == 0):
            clr.append(Color_Palette[0])
        else:
            clr.append(Color_Palette[6])
    return clr
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def create_map():
    day = mapping_day(days_options.active)
    hour = mapping_hour(slider.value)
    df['checkin_at_hour'] = checkin_at_hour(day, hour) #adds column df['checkin_at_hour'] for use in size calculation
    
    #checkin_vals = df['checkin_at_hour']
    sz = sizes(df['checkin_at_hour'])
    df['flag_1'] = selection_1(neighborhood.value)
    df['flag_2'] = selection_2(ambience.value)
    df['flag_3'] = selection_3(alcohol.value)
    df['flag_5'] = agg_selection(df['flag_1'],df['flag_2'],df['flag_3'])
    clr = colors(df['flag_5'])
    output_file("gmap.html")

    map_options = GMapOptions(lat=36.1200, lng=-115.1750, map_type="roadmap", zoom=11)

    p = gmap("AIzaSyBZ66UcTIUAyZBWhrhs8JLTzth9yMorgQU", map_options, title="Vegas", plot_width=800)
        
    source = ColumnDataSource(data=dict(lat=df['latitude'] ,lon=df['longitude'], size = sz, color = clr))

    p.circle(x="lon", y="lat", size="size", fill_alpha=0.6, fill_color = "color", line_width=1, line_alpha=0, hover_alpha = 0.8, source=source)
    
    return p

def create_chart():
    hour = list(range(0, 24))
    hour_str = []
    for x in hour:
        hour_str.append(str(x))

    avg_type = ['Overall', 'Selection']
    day = mapping_day(days_options.active)
    overall = average_checkins(day)
    data = {'hour' : hour_str,
            'Overall'   : overall}

    source = ColumnDataSource(data=data)

    b = figure(x_range=hour_str, y_range=(0, 30), title="Checkin Counts Comparison", toolbar_location=None, tools="", plot_width=800, plot_height=300)
    b.vbar(x=dodge('hour', -0.25, range=b.x_range), top='Overall', width=0.4, source=source,
           color="#718dbf", legend=value("Overall"))

    #b.vbar(x=dodge('hour', +0.25, range=b.x_range), top='Overall', width=0.2, source=source,color="#718dbf", legend=value("Overall"))

    #p.vbar(x=dodge('hour',  0.0,  range=p.x_range), top='Selection', width=0.2, source=source, color="#e84d60", legend=value("Selection"))

    b.x_range.range_padding = 0.1
    b.xgrid.grid_line_color = None
    b.legend.location = "top_left"
    b.legend.orientation = "horizontal"
    return b
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def update(attr, old, new):
    print(attr,"**",old,"**",new)
    layout.children[1].children[0] = create_map()
    layout.children[2] = create_chart()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#WIDGETS

days_options = RadioButtonGroup(labels=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], active=5)
days_options.on_change('active',update)

slider = Slider(start=0, end=23, value=0, step=1, title="Hour of Day")
slider.on_change('value',update)

#Select Options
neighborhood_options = list(set(df['neighborhood']))[1:]
alcohol_options = ['beer_and_wine', 'full_bar', 'none']
ambience = df['Ambience'][0]
ambience_options = [*ambience]

#Select Widgets
neighborhood = Select(title='Neighborhood', value='All', options= ['All'] + neighborhood_options)
neighborhood.on_change('value',update)
ambience = Select(title='Ambience', value='All', options=['All'] + ambience_options)
ambience.on_change('value',update)
alcohol = Select(title='Alcohol', value='All', options=['All'] + alcohol_options)
alcohol.on_change('value',update)
food_category = Select(title='Food Type', value='All', options=['All'])
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

time_control = widgetbox([days_options, slider], width = 400)
select_box = widgetbox(neighborhood, ambience, alcohol, food_category)
layout = column(time_control,row(create_map(),select_box), create_chart())
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

curdoc().add_root(layout)
curdoc().title = "Vegas"