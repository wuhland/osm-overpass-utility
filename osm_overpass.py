import sys
import re
import urllib2
import time
import os


def query_yes_no(question, default=None):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":True,   "y":True,  "ye":True,
             "no":False,     "n":False}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")

    
        
    

print("This program hopes to make scraping open street map a little easier by providing a very structured interface to the Overpass Web API. The API has some limitation in how much can be called (~100 million elements) so keep that in mind when you select your region of interest i.e. dont try to scrape the world. Also, you should probably have internet access if you want this to work.\n") 

#What would you like to name the output file
region = str(raw_input("Name the region you are interested in: "))
print("Now I am going to ask you for its bounding box. When entering the following information be aware that if your minimum longitude is bigger than your maximum longitude the bounding box will cross the longitude of 180 ")

def testInput(name):
    while True:
        try:
            variable = float(raw_input("Enter the " + name + " in decimal degrees: "))
        except ValueError:
            print "I dont understand. "
    
        else:
            return variable    
            break   

minLAT = testInput("min lat")

minLONG = testInput("min long")

maxLAT = testInput("max lat")

maxLONG = testInput("max long")


    

#bounding box as string in format minimum latitude, minimum longitude, maximum latitude, maximum longitude
bb = str(minLAT) + "," + str(minLONG) + "," + str(maxLAT) + "," + str(maxLONG) 

#while statement to continue taking feature input and exporting files until user says they are done
extract = True 

while extract:

    query = str(raw_input("Enter the feature you would like to scrape from OSM. Enter only one primary feature, you will be asked about classifications of that feature in a second (please review \"http://wiki.openstreetmap.org/wiki/Map_Features\" for suitable primary features): "))
    query.lower()

    test = query_yes_no("Would you like to query by a classification of the primary feature you just entered? ")

    if test is True:
        clas = str(raw_input("Enter the classification you would like to refine your scrape by (please check valid classifications @ \"http://wiki.openstreetmap.org/wiki/Map_Features\"): "))
        clas.lower()
        query = "%22" + query + "%22" + "=" + "%22" + clas + "%22"
    else:
        query = "%22" + query + "%22" 

    url = ("http://overpass-api.de/api/interpreter?data=[out:xml];(node["+ query +"]("+ bb + ");way[" + query + "]("+ bb + ");relation["+ query +"]("+ bb +"););(._;%3E;);out%20body;")

    print("requesting web resource")
    myRequest = urllib2.Request(url)
    print("reading data from resource")
    myUrlHandle = urllib2.urlopen(myRequest, timeout=90)

    #Create a file named region+query+date
    name = (region +"-" + query.replace("=","").replace("%22","") + "-" + time.strftime("%Y-%m-%d"+ ".osm"))

    f = open(name,'w')

    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(name)))

    print("writing data to "+ __location__)
    f.write(myUrlHandle.read()) 
    
    extract = query_yes_no("Would you like to extract another feature? (yes/no): ", default="no")
     

print("Ok. Hope you got what you came looking for. Adios. ")
