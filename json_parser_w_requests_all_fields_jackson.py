import json
from pprint import pprint
import csv
import requests

#api endpoint
url = "http://gis.co.jackson.mi.us/ArcGIS/rest/services/ParcelViewer/ParcelData/MapServer/identify"

#open list of mins and maxes
csv_reader = csv.reader(open('jackson_all_mins_maxes.csv'))

#get list of fields to populate values for
filename = "fields_available_jackson.txt"
list_of_fields = open(filename).read().splitlines()
list_of_fields.append("geometry")

cur_row = 1
for min_max_row in csv_reader:

    min_max_str = ','.join(str(e) for e in min_max_row)

    # defining a params dict for the parameters to be sent to the API
    params = {'f':'json', 'returnGeometry': 'true', 'geometry': min_max_str, 'geometryType':'esriGeometryEnvelope','tolerance':'6','mapExtent': min_max_str,'imageDisplay':'964,541,96'}

    # sending get request and saving the response as response object
    r = requests.get(url = url, params = params)
     
    # extracting data in json format
    data = r.json()

    list_of_rows = []
    #if list of results is not empty
    if len(data["results"]) != 0 :
        for each in data["results"]:
            list_of_cells = []
            for field in list_of_fields:
                if field == "geometry":
                    continue
                else:
                    list_of_cells.append(each["attributes"][field])
            list_of_cells.append(each["geometry"])
            list_of_rows.append(list_of_cells)
        print(len(list_of_rows))
    else:
        list_of_rows.append("No results")

    outfile_name = str.join("", ["jackson_row_", str(cur_row)])
    outfile = open(str.join("",["./",outfile_name,".csv"]), "w")
    writer = csv.writer(outfile)
    writer.writerow(list_of_fields)
    writer.writerows(list_of_rows)
    cur_row += 1