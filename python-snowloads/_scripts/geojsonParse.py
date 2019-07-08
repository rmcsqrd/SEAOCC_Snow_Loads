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
# this website is really helpful to visualize data structure http://jsonviewer.stack.hu/

features = data['features']  # list of dictionaries
mapDict = {}  # final output dict to be written into leaflet format

for cnt, item in enumerate(features):  # step through all values within file, note this includes county data as well
    for k, v in item.items():  # step into the 'geometry', 'properties', and 'type' dicts

        if item['properties']['description'] is not None:  #  get a title for the dictionary - we only want values that have a description
            description = item['properties']['description']
            title = re.search("(?<=<p>)(.*?)(?=<\/p>)", description).group(0)  # regex code hacked together from stack overflow
            title = title.replace(' ', '')

            if 'geometries' in item['geometry']:  # some containers are empty and return error
                if item['geometry']['geometries'][0]['type'] is not 'Point':  # coords have arbitrary (?) point data
                    coords = item['geometry']['geometries'][1]['coordinates'][0]  # coords are nested a few times
                    for subitem in coords:
                        subitem.reverse() # very confusing but coordinates are flipper apparently

        mapDict[title] = [description, coords]

## Write to file ##

# this is where I got really lazy - need to update this in the future when we have more time
file = open(dataWriteDirectory+"leaflet_input.txt","w")
for k,v in sorted(mapDict.items()):
    print(k)
    file.write('var '+ k + ' = L.polygon([\n')
    for cnt, item in enumerate(v[1]):  # really unelegant method for not adding a comma to end
        if (cnt+1) != len(v[1]):
            file.write('%s' % item +',\n')
        else:
            file.write('%s' % item + '\n')
    file.write(']).addTo(mymap);')
    file.write('\n')
    file.write(k + '.bindPopup("' + v[0] + '");')
    file.write('\n\n')
file.close()
