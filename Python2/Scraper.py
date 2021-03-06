#!/usr/bin/python2

## Written by LAMMJohnson
## If something goes wrong, it's your fault so eat shit.

import os, sys, urllib, re, getopt
from time import time, sleep

## Defaults
verbose = True
output = "./"
refresh = 10

## Globals
downtot = 0

##Functions
def v_print(instr):
    if verbose:
        print instr

def usage():
    v_print("==================================================")
    v_print("Usage: Scraper-Python2 [OPTION] <thread url>")
    v_print("Default OPTIONS: --output ./ --thread 10")
    v_print("Bash script to scrape 4chan, part of 4chantoolbox.")
    v_print("")
    v_print(" -o/--output set output dir")
    v_print(" -q/--quiet go silent")
    v_print(" -t/--timer N thread refresh timer")
    v_print(" -h/--help this message")
    v_print("")
    v_print("insert <witty comment> here")
    v_print("==================================================")
    sys.exit(' ')

## Handle URL arg
if len(sys.argv) == 1:
    usage()
else:
    url = sys.argv[len(sys.argv) - 1]

## Handle flags
try:                                
    opts, args = getopt.gnu_getopt(  sys.argv, "hqo:t:", \
                                       ["help", "quiet", "output", "timer"])
except getopt.GetoptError:
    v_print (str(err))
    usage()

for o, a in opts:
    if o == "-q":
        verbose = False
    elif o in ("-h", "--help"):
        usage()
    elif o in ("-o", "--output"):
        output = a
    elif o in ("-t", "--timer"):
        refresh = int(a)
    else:
        assert False, "Unhandled Option"

##Error check the given path
if os.path.isdir(output) == False:
    print "Given output location '" + output + "' is not a directory. EXITING!"
    sys.exit(' ')

##Report which options we're using
v_print("Downloading " + url)
v_print("Saving to location " + output)
v_print("Timer set to every " + str(refresh) + " seconds.")

## Main loop
while 1:
    try:
        lasttime = time()

        # Grab the page and split out the image URLS
        html = urllib.urlopen(url);
        v_print("Page " + url + " downloaded. Processing images.")
        images = re.findall('http://images.4chan.org/(?:[a-zA-z]{1,4}|3)/src/\d{13}.(?:png|gif|jpg)', html.read())

        for image in images:
            # Split the image name from the URL and get a full path to write to
            imagename = re.search('src/(.*$)', image)
            imagename = imagename.group(1)
            fullpath = os.path.join(output, imagename)

            # Get the file if necessary
            if os.path.exists(fullpath):
                v_print("File " + fullpath + "' exists. Skipping.")
            else:
                v_print("Getting " + image)
                u = urllib.urlopen(image)
                localFile = open(fullpath, 'w')
                localFile.write(u.read())
                localFile.close()
                downtot += 1

        # Timer
        looptime = int(time() - lasttime);
        lasttime = time();
        v_print("Finished in " + str(looptime) + " seconds.")
        if looptime < refresh:
            v_print("Sleeping for " + str(refresh - looptime) + " seconds.")
            sleep (refresh - looptime)

    # Handle the keyboard interrupt event
    except (KeyboardInterrupt, SystemExit):
        print "\nInterupted. "  + str(downtot) + " pics downloaded in total from " + url
        sys.exit('')
