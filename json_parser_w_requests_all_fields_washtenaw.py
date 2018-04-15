import json
from pprint import pprint
import csv
import requests

#api endpoint
url = "https://webmapssecure.ewashtenaw.org/arcgisshared/rest/services/OverlayQuery/MapServer/0/query"

#api token
token = "8wBWQHniIj5r34ZciByCCO5yAA1oD2iaaXaJJckGPbY."

#open list of polygons
csv_reader = csv.reader(open('washtenaw_last_101.csv'))

#get list of fields to populate values for
filename = "webscraping_fields_available.txt"
list_of_fields = open(filename).read().splitlines()
list_of_fields.append("geometry")

cur_row = 11706
for polygon_row in csv_reader:

    polygon_list_to_str = str.join(',', polygon_row)
    if polygon_list_to_str[-1] == ",":
        polygon_list_to_str = polygon_list_to_str[:-1]
    polygon = str.join("", ["[[", polygon_list_to_str, "]]"])
    geometry_param = str.join("", ["{\"rings\":", polygon, ",", "\"spatialReference\":{\"wkid\":2253}}"])
    # defining a params dict for the parameters to be sent to the API
    params = {'token':token, 'f':'json', 'returnGeometry': 'true', 'spatialRel':'esriSpatialRelIntersects', 'geometry': geometry_param, 'geometryType':'esriGeometryPolygon','inSR':'2253','outFields':'*','outSR':'2253'}

    # sending get request and saving the response as response object
    r = requests.get(url = url, params = params)
     
    # extracting data in json format
    data = r.json()

    list_of_rows = []
    for each in data["features"]:
        list_of_cells = []
        for field in list_of_fields:
            if field == "geometry":
                continue
            else:
                list_of_cells.append(each["attributes"][field])
        list_of_cells.append(each["geometry"])
        list_of_rows.append(list_of_cells)

    outfile_name = str.join("", ["row", str(cur_row)])
    outfile = open(str.join("",["./",outfile_name,".csv"]), "w")
    writer = csv.writer(outfile)
    writer.writerow(list_of_fields)
    writer.writerows(list_of_rows)
    cur_row += 1