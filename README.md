## Example usages:
#### python elev.py input.csv output.csv
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Takes input from input.csv and saves the output in output.csv.
#### python elev.py input.csv -
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Takes input from input.csv and prints the output to stdout.

## Optional flags:

#### -h, --help
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Shows help message and exit. Does not process any input.

#### --no_status
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;DOES NOT print how many locations were processed (No option means printing info)

#### --only_elev
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Output contain only elevation values.

## Required input file format

Input file should contain:
1. Headers (labels) in the very first line, separated with comma
2. Headers MUST contain at least "lat" and "lon" at whichever position
3. One point data per one line
4. Data line MUST contain lattitude and longtitude value at the same position as "lat" and "lon" headers

Check test.csv or 20170607154138.csv files to see examples
