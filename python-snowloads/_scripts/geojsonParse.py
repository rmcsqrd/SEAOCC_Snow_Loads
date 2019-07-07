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


        # parse out written description
        description = None  # assign blank variable for description so no error if "None"
        if k == 'properties':
            if None != v['description']:
                description = v['description']

        # parse out coordinates
        coords = None
        if k == 'geometry':
            if v.get('geometries') is not None:  # some containers are empty and return error
                for geometryContainer in v.get('geometries'):
                    if geometryContainer.get('type') != 'Point':  # coords have arbitrary (?) point data
                        coords = geometryContainer['coordinates'][0]  # coords are nested a few times

        #  get a title for the dictionary - we only want values that have a description
        title = None
        if description:  # non-empty strings return TRUE
            title = re.search("(?<=<p>)(.*?)(?=<\/p>)", description).group(
                0)  # regex code hacked together from stack overflow
            title = title.strip()

        # cobble it all together
        mapDict[title] = [description, coords]
    # print(title, description[1:10], coords[1:10])
for k, v in mapDict.items():
    print(k, v)

