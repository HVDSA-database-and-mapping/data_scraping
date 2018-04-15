import csv

#I had a file called "temp nodes copy" (now deleted) just in case something went wrong with "temp nodes good"
#csv_reader = csv.reader(open('jackson_2nd_div_latest_try.csv'))

list_of_mins_maxes = []
last_index = -1

with open('livingston_2nd_div_coords.csv') as f:
    csv_reader = csv.DictReader(f, delimiter=',')
    for row in csv_reader:
        index = float(row["shapeid"])
        x = float(row["x"])
        y = float(row["y"])
        if last_index != index:
            first_x = x
            first_y = y
            xmin = x
            ymin = y
            xmax = x
            ymax = y
    
        if x < xmin:
            xmin = x
        if y < ymin:
            ymin = y
        if x > xmax:
            xmax = x
        if y > ymax:
            ymax = y

        if (first_x == x) and (first_y == y) and (index == last_index):
            list_of_mins_maxes.append([xmin,ymin,xmax,ymax])
        last_index = float(row["shapeid"])

#"new all polygons "includes all the points
#"all polygons" always only had 5 pts no matter how many there actually were
outfile_name = "livingston_mins_maxes"
outfile = open(str.join("",["./",outfile_name,".csv"]), "w")
writer = csv.writer(outfile)
writer.writerows(list_of_mins_maxes)