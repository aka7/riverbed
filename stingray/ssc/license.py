#! /usr/bin/env python  
# adding a stm instance to ssc controller as non-managed
# once added, you need to install the FLA key on the instance.
import requests  
import json  
import sys,os  
import ssc_common
from optparse import OptionParser
from ssc_common import getSSCURI,getPassword,sscConnection,listurl,showResource


# provide FQDN stm name to be created as non-managed on ssc 
# set license keyi and bandwidth for this stm

def addLic(ljson,license):
	uri=getSSCURI()
	url = uri+'license/' + license
	jsontype = {'content-type': 'application/json'}  
	  
	client =  sscConnection()
	try:  
	    #First see if the license resource already exists  
	    response = client.get(url)  
	except requests.exceptions.ConnectionError:  
	    print "Error: Unable to connect to " + url  
	    sys.exit(1)  
	if (response.status_code == 404):  
	    response = client.put(url, data = json.dumps(ljson), headers = jsontype)  
	    if response.status_code == 201: # When creating a new resource we expect to get a 201  
	        print 'license %s added' %(license)  
	        response = client.get(url)  
		print response.content
	    else:  
	        data = json.loads(response.content)  
	        print "Error adding instance %s: URL=%s Status=%d Id=%s: %s" %(license, url, response.status_code, data['error_id'], data['error_info'])  
	else:  
	    if response.status_code == 200:  
	        print "license %s already exists" %(license)  
	    else:  
	        print "Error: Status=%d URL=%s" %(response.status_code, url)    

def main():
    	parser = OptionParser(version='0.1')
    	parser.add_option("--debug", dest="debug",
    	    default=False,
    	    help="Show debugging")

    	parser.add_option("-l", "--license", dest="lname",
        	default=None,
        	help="license name")
    	parser.add_option("-s", "--show licenses", dest="list",
		action="store_true",default=False,
        	help="show current licenses")
        parser.add_option("-u", "--username", dest="username",
        	default=None,
        	help="username for api access")
	parser.add_option("-q", "--query", dest="query",
        	default=None,
        	help="list resource of a given license")

    	(options, args) = parser.parse_args()
    	if options.debug:
		global debug
		debug = True
    	username='sscadmin'
    	if not options.username is None:
		username = options.username
        	ssc_common.username=username

    	if options.list:
    		listurl('license')
		sys.exit(0)
    	if options.query:
    		showResource(options.query)
		sys.exit(0)

    	if (options.lname is None):
    	    print >> sys.stderr, "provide name for license resource"
    	    sys.exit(1)

	
	lname=options.lname

	licensejson={
	"info": "This is the resource for fla "+lname+" license",
	}
	if not options.list:
		addLic(licensejson,lname)
	

	

if __name__ == "__main__":
    main()
