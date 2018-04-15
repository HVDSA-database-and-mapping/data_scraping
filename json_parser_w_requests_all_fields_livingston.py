import json
from pprint import pprint
import csv
import requests

#api endpoint
url = "https://utility.arcgis.com/usrsvcs/servers/a3076b544a3d44ccb2c34f23b2533f6a/rest/services/AGO/Parcels/MapServer/6/query"
headers = dict()
headers["Origin"] = "https://livgov.maps.arcgis.com"
headers["X-DevTools-Emulate-Network-Conditions-Client-Id"] = "(57370BE297DFAC75BC18F0101C28AA7B)"
headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
headers["Accept"] = "*/*"
headers["Referer"] = "https://livgov.maps.arcgis.com/apps/webappviewer/index.html?id=f3cd4da87c034c3eb8ba892da94c47f6"
headers["Accept-Encoding"] = "gzip, deflate, br"
headers["Accept-Language"] = "en-US,en;q=0.9"
headers["DNT"] = "1"


#open list of mins and maxes
csv_reader = csv.reader(open('livingston_mins_maxes.csv'))

#get list of fields to populate values for
filename = "livingston_fields_available.txt"
list_of_fields = open(filename).read().splitlines()
list_of_fields.append("geometry")

cur_row = 1
for min_max_row in csv_reader:

    min_max_str = ','.join(str(e) for e in min_max_row)

    # defining a params dict for the parameters to be sent to the API
    params = dict()
    params["f"] = 'json'
    params["returnGeometry"] = 'true' 
    params["geometry"] = min_max_str
    params["'geometryType"] = 'esriGeometryEnvelope'
    params["spatialRel"] = 'esriSpatialRelIntersects'
    params["inSR"] = "102100"
    params["outFields"] = "*"
    params["outSR"] = "102100" 

    # sending get request and saving the response as response object
    r = requests.get(url = url, params = params, headers = headers)
     
    # extracting data in json format
    data = r.json()
    if "error" in data.keys():
        print(data)
        exit()

    list_of_rows = []
    #if list of results is not empty
    if len(data["features"]) != 0 :
        for each in data["features"]:
            list_of_cells = []
            for field in list_of_fields:
                if field == "geometry":
                    continue
                else:
                    list_of_cells.append(each["attributes"][field])
            list_of_cells.append(each["geometry"])
            print(list_of_cells)
            list_of_rows.append(list_of_cells)
    else:
        list_of_rows.append("No results")

    outfile_name = str.join("", ["livingston_row_", str(cur_row)])
    outfile = open(str.join("",["./",outfile_name,".csv"]), "w")
    writer = csv.writer(outfile)
    writer.writerow(list_of_fields)
    writer.writerows(list_of_rows)
    cur_row += 1