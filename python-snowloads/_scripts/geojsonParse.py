## Imports/Globals ##
import os
import json
import re

## Directory Locations ##

os.chdir("//Users//riomcmahon//Programming//snowloads//support//data")
dataGetDirectory = "//Users//riomcmahon//Programming//snowloads//support//original_kmz//"
dataWriteDirectory = "//Users//riomcmahon//Programming//snowloads//support//data//"

## Load JSON ##

with open(dataGetDirectory+"Counties_April_20.geojson","r") as file:
    data = json.load(file)

## Parse JSON ##

# RAW DATA ORGANIZATION
# this website is also really helpful http://jsonviewer.stack.hu/

# features (list)
#     geometry (dict)
#         --> type
#             --> Geometry Collection
#         --> geometries
#             --> Point
#             --> Polygon/Multipolygon ***these are the coordinates we want
#     properties (dict)
#         --> Name
#         --> HAWN_PI
#         --> OTHER
#         --> AMERI_ES
#         --> description ***this is the description we want
#         --> HISPANIC
#         --> snippet
#         --> WHITE
#         --> POP00_SQMI
#         --> MALES
#         --> BLACK
#         --> FEMALES
#         --> tessellate
#         --> visibility
#         --> POP2000
#         --> MULT_RACE
#         --> ASIAN
#         --> SQMI
#     type (str)
#         --> Feature (this is just a descriptor, doesn't contain any information)

features = data['features']  # list of dictionaries
mapDict = {}  # final output dict to be written into leaflet format

for cnt, item in enumerate(features):  # step through all values within file, note this includes county data as well
    for k, v in item.items():  # step into the 'geometry', 'properties', and 'type' dicts

        if item['properties']['description'] is not None:  #  get a title for the dictionary - we only want values that have a description
            description = item['properties']['description']
            title = re.search("(?<=<p>)(.*?)(?=<\/p>)", description).group(0)  # regex code hacked together from stack overflow

            if 'geometries' in item['geometry']:  # some containers are empty and return error
                if item['geometry']['geometries'][0]['type'] is not 'Point':  # coords have arbitrary (?) point data
                    coords = (item['geometry']['geometries'][1]['coordinates'])  # coords are nested a few times
        mapDict[title] = [description, coords]

for k, v in mapDict.items():
    print(k, v)