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
