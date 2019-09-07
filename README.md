# CS590-Yelp

- To convert json to csv

json_to_csv_converter: Convert the dataset from json format to csv format.

$ python json_to_csv_converter.py yelp_academic_dataset.json # Creates yelp_academic_dataset.csv

-Vegas.py is the main bokeh file for the Geospatial Visualization and Checkin Barchart along with interaction widgets.
-Run Vegas.py on terminal using command "bokeh serve --show vegas.py
-Two additional features need to be added to the vegas.py code as of now (barchart glyph for specific selection & food selection widget)

-The above file runs off of nevada_cleaned.csv. 
-The criteria used for filtering in nevada_cleaned.csv is category == 'Restaurant' && review_count > 50.
-Additionally, another important feature of the nevada_cleaned.csv file is the extraction of checkin counts from a 
messed up format provided by yelp to a format that could easily be converted into a python dictionary in the code.


## Final Details to Run:

Files to run - RunMe.py
Consists of the cleaning of businesses data, all plot, layout, widget creation and updation

Preprocessing.py
Consists cleaning of user data, layout design and color mapping for the nodes.

Data Sizes 
Businesses - 6MB
Network - 7MB (Includes color mapped to nodes and layout position of nodes. Original data used is 5MB.)

Server Requirements:

Bokeh disconnects the server connection if the data being transferred is more than 20 MB.
A workaround to overcome this is to mention the data limit (to say 50MB) which running such as:
bokeh serve --show RunMe.py --websocket-max-message-size 52428800

This feature is present only for the recent bokeh version. For older version, the file tornado.py in the bokeh package should be edited as follows:
At line 263: (original code)
super(BokehTornado, self).__init__(all patterns)

Changes to:
super(BokehTornado, self).__init__(all_patterns, websocket_max_message_size=50*1024*1024, **kwargs)
