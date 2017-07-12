import urllib.request
import json
import argparse
import sys
from argparse import RawTextHelpFormatter


API_KEY ='AIzaSyAN7atisvzb23HTyefcAKP9nc5nwNAe9HA'
LOC_PER_REQ = 256   # safe amount. 512 would be accepted, but URLs are too long then ( over 8096 characters )
                    # Max available value is calculated, so 256 will be replaced anyway


parser = argparse.ArgumentParser(description="""
Example usages:
1. python elev.py 20170607154138.csv out.csv
    Takes input from 20170607154138.csv and saves the output in out.csv.
2. python elev.py 20170607154138.csv -
    Takes input from 20170607154138.csv and prints the output to stdout.

Optional flags:

--no_status - DOES NOT print how many locations were processed (No option means printing info)
--only_elev - Output contain only elevation values.

""", formatter_class=RawTextHelpFormatter)
parser.add_argument('input_file', help="File with input locations.")
parser.add_argument('output_file', help="File which results will be written to. For standard output type: -")
parser.add_argument('--only_elev', help="Only elevation values are printed to output file", action="store_true")
parser.add_argument('--comma_style', help="[NOT IMPLEMENTED YET]Prints floating point values with comma, and space as a separator", action="store_true")
parser.add_argument('--no_status', help="With this flag, script WILL NOT print out how many locations were processed", action="store_true")

args = parser.parse_args()

locations = []
elevations = []

# Import data from file
with open(args.input_file) as f:
    f.readline() # skip first line
    for line in f.readlines():
        line = line.strip(' \n\r\t')
        lat, lng = line.split(',')[1], line.split(',')[2]
        lat, lng = lat.strip(), lng.strip()
        locations.append( (lat,lng) )


# Calculate max available amount of locations in one request
chars_left = 8096 - len("https://maps.googleapis.com/maps/api/elevation/json?locations=") - len("&key=" + API_KEY)
LOC_PER_REQ = int(chars_left/len(lat + ',' + lng + '|'))


# Calculate number of requests required to complete the task
number_of_requests = int(len(locations)/LOC_PER_REQ) + 1


# Get elevation values for every location
counter = 0
for i in range(number_of_requests):
    counter += len(locations[i*LOC_PER_REQ:(i+1)*LOC_PER_REQ])
    
    # Create URL string
    url = "https://maps.googleapis.com/maps/api/elevation/json?locations="
    for location in locations[i*LOC_PER_REQ:(i+1)*LOC_PER_REQ]:
        lat, lng = location
        url += lat + ',' + lng + '|'
    url = url[:-2]
    url += '&key=' + API_KEY

    # Get responses and append elevations to the list
    response = json.loads(urllib.request.urlopen(url).read())
    
    for result in response['results']:
        elevations.append(result['elevation'])

    if not args.no_status:
        print('Processed:',counter,"locations") #console log


# Make sure that we got elevation value for each location
assert len(locations) == len(elevations)


# Print output
if args.output_file is not '-' :
    file_out = open(args.output_file, 'w')
else:
    file_out = sys.stdout

with open(args.input_file) as file_in: # Open input file again to rewrite lines

    # First line (headers)
    line = file_in.readline()
    line = line.replace('\n', '') if '\n' in line else line
    print(line + ',elevationfixed', file=file_out)

    # Data
    for elevation in elevations:
        if args.only_elev:
            print(str(elevation), file=file_out)
        else:
            line = file_in.readline()
            line = line.replace('\n', '') if '\n' in line else line
            print(line + ',' + str(elevation), file=file_out)
            
file_out.close()

