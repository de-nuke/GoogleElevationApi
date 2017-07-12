import urllib.request
import json
import argparse
import sys
from argparse import RawTextHelpFormatter

API_KEY ='AIzaSyAN7atisvzb23HTyefcAKP9nc5nwNAe9HA'
LOC_PER_REQ = 256 # safe amount. 512 would be accepted, but URLs are too long then ( over 8096 characters )

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
parser.add_argument('--no_status', help="With this flag, script WILL NOT print out how many locations were processed", action="store_true")
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
    f.readline() # skips first line
    for line in f.readlines():
        line = line.strip(' \n\r\t')
        lat, lng = line.split(',')[1], line.split(',')[2]
        lat, lng = lat.strip(), lng.strip()
        locations.append( (lat,lng) )

chars_left = 8096 - len("https://maps.googleapis.com/maps/api/elevation/json?locations=") - len("&key=" + API_KEY)
LOC_PER_REQ = int(chars_left/len(lat + ',' + lng + '|'))


# Calculates number of requests required to complete the task
number_of_requests = int(len(locations)/LOC_PER_REQ) + 1

# Gets elevation values for every location

counter = 0
for i in range(number_of_requests):
    counter += len(locations[i*LOC_PER_REQ:(i+1)*LOC_PER_REQ])
    
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

    if not args.no_status:
        print('Processed:',counter,"locations") #console log

# Makes sure that we got elevation value for each location
assert len(locations) == len(elevations)

points = list(zip(locations, elevations))


if args.output_file is not '-' :
    file_out = open(args.output_file, 'w')
else:
    file_out = sys.stdout

with open(args.input_file) as file_in:
    line = file_in.readline()
    line = line.replace('\n', '') if '\n' in line else line
    print(line + ',elevationfixed', file=file_out)
    
    for point in points:
        lat, lng = point[0]
        elevation = str(point[1])
    
        if args.only_elev:
            print(elevation, file=file_out)
        else:
            line = file_in.readline()
            line = line.replace('\n', '') if '\n' in line else line
            print(line + ',' + elevation, file=file_out)
##            print(file_in.readline() + elevation, file=file_out)

    file_out.close()

