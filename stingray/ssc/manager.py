#! /usr/bin/env python  
# to change ssc manager settings.

import requests  
import json  
import sys,os  
from optparse import OptionParser
import ssc_common
from ssc_common import getSSCURI,getPassword,sscConnection,listurl,showResource


# provide FQDN stm name to be created as non-managed on ssc 
# set license keyi and bandwidth for this stm
def updateManager(managerhost,managerjson):
	uri=getSSCURI()
	url = uri+'manager/' + managerhost
	jsontype = {'content-type': 'application/json'}  
	  
	client = sscConnection()
  
	try:  
	    #First see if the license resource already exists  
	    response = client.get(url)  
	except requests.exceptions.ConnectionError:  
	    print "Error: Unable to connect to " + url  
	    sys.exit(1)  
	if (response.status_code == 404):  
	    print "Manager %s does not exists" %(managerhost)
	else:  
	    if response.status_code == 200:  
	        print "manager %s, Enabling license" %(managerhost)  
	    	response = client.put(url, data = json.dumps(managerjson), headers = jsontype)  
	    	if response.status_code == 200: # When update a new resource we expect to get a 200
			print 'manager %s updated' %(managerhost)  
	    		response = client.get(url)  
			print response.content
	    	else:
	    		print 'cannot enable license for manager  %s' %(managerhost)  
	    	    	data = json.loads(response.content)  
	        	print "Error enabling manager for license %s: URL=%s Status=%d Id=%s: %s" %(managerhost, url, response.status_code, data['error_id'], data['error_text'])  
	    else:  
	        print "Error: Status=%d URL=%s" %(response.status_code, url)    
	
def main():
    parser = OptionParser(version='0.1')
    parser.add_option("--debug", dest="debug",
        default=False,
        help="Show debugging")

    parser.add_option("-n", "--notreally", dest="not_really",
        default=False,
        help="Don't create anything")

    parser.add_option("-i", "--update-ssc", dest="sscva_name",
        default=None,
        help="update given ssc manager instance")
    parser.add_option("-l", "--lic", dest="license",
        default=None,
        help="set licensing to eihter enabled/disabled")
    parser.add_option("-m", "--metering", dest="metering",
        default=None,
        help="set metering, to all/none")
    parser.add_option("-s", "--show", dest="show",
        action="store_true",default=False,
        help="list all current manager resouce")
    parser.add_option("-q", "--query", dest="query",
        default=None,
        help="list resource of a given instance")
    parser.add_option("-u", "--username", dest="username",
        default=None,
        help="username for api access")
    parser.add_option("-p", "--pass", dest="adminpass",
        action="store_true",default=False,
        help="stm instance admin password for rest api")

    (options, args) = parser.parse_args()
    if options.debug:
        global debug
        debug = True

    username='sscadmin'
    if not options.username is None:
	username = options.username
    ssc_common.username=username

    if options.show:
    	listurl('manager')
        sys.exit(0)

    if not options.query is None:
	showResource(options.query)
        sys.exit(0)
	
    if (options.sscva_name is None) and  (not options.show ):
        print >> sys.stderr, "provide manager name to update"
        sys.exit(1)
    if (options.license is None) and (options.metering is None):
        print >> sys.stderr, "Need to provide ether meeting or licensing options to change."
        sys.exit(1)

    
    managerjson={}
    if not options.license is None:
    	managerjson={
		"licensing": options.license
        }
    if not options.metering is None:
    	managerjson={
		"metering": options.metering
        }

    if (not options.license is None) and (not options.metering is None):

	    managerjson={
		"licensing": options.license,
		"metering": options.metering
	    }
	
    if not options.show:
    	updateManager(options.sscva_name,managerjson)

if __name__ == "__main__":
    main()

