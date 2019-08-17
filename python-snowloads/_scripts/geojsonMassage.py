## Imports/Globals ##
import os
import json
import re

## Directory Locations ##

os.chdir("//Users//riomcmahon//Programming//snowloads//support//data")
dataGetDirectory = "//Users//riomcmahon//Programming//snowloads//support//original_kmz//"
dataWriteDirectory = "//Users//riomcmahon//Programming//snowloads//support//data//"

## Load JSON ##

with open(dataGetDirectory+"Placer_County.geojson","r") as file: # use this to change the filename
    data = json.load(file)

## Parse JSON ##
# this website is really helpful to visualize data structure http://jsonviewer.stack.hu/

features = data['features']  # list of dictionaries

for cnt, item in enumerate(features):  # step through all values within file, note this includes county data as well
    for k, v in item.items():  # step into the 'geometry', 'properties', and 'type' dicts

        if item['properties']['description'] is not None:  #  update "Name" in geoJSON container
            description = item['properties']['description']
            title = re.search("(?<=<p>)(.*?)(?=<\/p>)", description).group(0)  # determine county ID
            item['properties']['Name'] = title.replace(" ","")  # append county ID with no space so we can use as filename

            if 'geometries' in item['geometry']:  # some containers are empty and return error
                if item['geometry']['geometries'][0]['type'] == 'Point':  # coords have point data marker for county, remove this
                    del item['geometry']['geometries'][0]
    with open(dataWriteDirectory+title.replace(" ","")+".json", "w") as outfile: # write files to a directory
        json.dump(item,outfile)


# ## Write to file ##
#
# # this is where I got really lazy - need to update this in the future when we have more time
# file = open(dataWriteDirectory+"leaflet_input.txt","w")
# for k,v in sorted(mapDict.items()):
#     print(k)
#     file.write('var '+ k + ' = L.polygon([\n')
#     for cnt, item in enumerate(v[1]):  # really unelegant method for not adding a comma to end
#         if (cnt+1) != len(v[1]):
#             file.write('%s' % item +',\n')
#         else:
#             file.write('%s' % item + '\n')
#     file.write(']).addTo(mymap);')
#     file.write('\n')
#     file.write(k + '.bindPopup("' + k + '");')
#     file.write('\n\n')
# file.close()