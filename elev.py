import urllib.request
import json
import argparse
import sys
from argparse import RawTextHelpFormatter

API_KEY ='AIzaSyAN7atisvzb23HTyefcAKP9nc5nwNAe9HA'
LOC_PER_REQ = 512

parser = argparse.ArgumentParser(description="""
*******
Returns elevation values for input locations. Required input format is:
lat1,lng1
lat2,lng2
...
etc.

example:
52.226488,21.001362
52.211878,20.962028
52.268324,20.800880

Any whitespaces beetwen numbers and comma or at the begining and end of line are omitted.
*******
""", formatter_class=RawTextHelpFormatter)
parser.add_argument('input_file', help="File with input locations.")
parser.add_argument('output_file', help="File which results will be written to. For standard output type: -")
parser.add_argument('--only_elev', help="Only elevation values are printed to output file", action="store_true")
parser.add_argument('--comma_style', help="[NOT IMPLEMENTED YET]Prints floating point values with comma, and space as a separator", action="store_true")
action = parser.add_mutually_exclusive_group(required=False)
action.add_argument('--sort_lat_asc', help="[NOT IMPLEMENTED YET]Sorting points ascending by lattitude.", action="store_true")
action.add_argument('--sort_lat_desc', help="[NOT IMPLEMENTED YET]Sorting points descending by lattitude.", action="store_true")
action.add_argument('--sort_lng_asc', help="[NOT IMPLEMENTED YET]Sorting points ascending by longtitude.", action="store_true")
action.add_argument('--sort_lng_desc', help="[NOT IMPLEMENTED YET]Sorting points descending by longtitude.", action="store_true")
action.add_argument('--sort_elev_asc', help="[NOT IMPLEMENTED YET]Sorting points ascending by elevation.", action="store_true")
action.add_argument('--sort_elev_desc', help="[NOT IMPLEMENTED YET]Sorting points descending by elevation.", action="store_true")

args = parser.parse_args()

locations = []
elevations = []

# Imports data from file
with open(args.input_file) as f:
    for line in f.readlines():
        line = line.strip(' \n\r\t')
        lat, lng = line.split(',')
        lat, lng = lat.strip(), lng.strip()
        locations.append( (lat,lng) )

# Calculates number of requests required to complete the task
number_of_requests = int(len(locations)/LOC_PER_REQ) + 1

# Gets elevation values for every location
for i in range(number_of_requests):
    
    # Creates URL string
    url = "https://maps.googleapis.com/maps/api/elevation/json?locations="
    for location in locations[i*LOC_PER_REQ:(i+1)*LOC_PER_REQ]:
        lat, lng = location
        url += lat + ',' + lng + '|'
    
    url = url[:-2]
    url += '&key=' + API_KEY

    # Gets responses and appends elevations to the list
    response = json.loads(urllib.request.urlopen(url).read())

    for result in response['results']:
        elevations.append(result['elevation'])

# Makes sure that we got elevation value for each location
assert len(locations) == len(elevations)

points = list(zip(locations, elevations))


if args.output_file is not '-' :
    file = open(args.output_file, 'w')
else:
    file = sys.stdout

for point in points:
    lat, lng = point[0]
    elevation = str(point[1])
    
    if args.only_elev:
        print(elevation, file=file)
    else:
        print(lat + ',' + lng + ',' + elevation, file=file)

file.close()

