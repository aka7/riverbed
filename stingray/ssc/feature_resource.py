#! /usr/bin/env python  
# adding a stm instance to ssc controller as non-managed
# once added, you need to install the FLA key on the instance.
import requests  
import json  
import sys,os  
import ssc_common
from optparse import OptionParser
from ssc_common import getSSCHost,getPassword,sscConnection,listurl,showResource,getSSCURI

username='admin'

def addFeature(fjson,fpack):

	client=sscConnection()
	uri=getSSCURI()
	url = uri+'feature_pack/'+fpack
	jsontype = {'content-type': 'application/json'}  
  
	try:  
	    #First see if the fpack resource already exists  
	    response = client.get(url)  
	except requests.exceptions.ConnectionError:  
	    print "Error: Unable to connect to " + url  
	    sys.exit(1)  
	if (response.status_code == 404):  
	    response = client.put(url, data = json.dumps(fjson), headers = jsontype)  
	    if response.status_code == 201: # When creating a new resource we expect to get a 201  
	        print 'fpack %s added' %(fpack)  
	        response = client.get(url)  
		print response.content
	    else:  
	        data = json.loads(response.content)  
	        print "Error adding feature pack %s: URL=%s Status=%d Id=%s: %s" %(fpack, url, response.status_code, data['error_id'], data['error_info'])  
	else:  
	    if response.status_code == 200:  
	        print "fpack %s already exists" %(fpack)  
	    else:  
        	print "Error: Status=%d URL=%s" %(response.status_code, url)    

def main():
    	parser = OptionParser(version='0.1')
    	parser.add_option("--debug", dest="debug",
    	    default=False,
    	    help="Show debugging")

    	parser.add_option("-f", "--fpack", dest="fpack",
        	default=None,
        	help="name for the feature pack")
    	parser.add_option("-k", "--sku", dest="skuname",
        	default=None,
        	help="name of the sku for this feature pack")
    	parser.add_option("-s", "--show feature pack and stm_sku", dest="list",
		action="store_true",default=False,
        	help="show current feature packs")
        parser.add_option("-u", "--username", dest="username",
        	default=None,
        	help="username for api access")
	parser.add_option("-q", "--query", dest="query",
        	default=None,
        	help="list resource of a given feature")

    	(options, args) = parser.parse_args()
    	if options.debug:
		global debug
		debug = True


    	username='sscadmin'
    	if not options.username is None:
		username = options.username
		ssc_common.username=username
    	if options.list:
    		listurl('feature_pack')
		print '####### SKU LIST #########'
    		listurl('sku')
		sys.exit(0)
	
    	if not options.query is None:
		showResource(options.query)
		sys.exit(0)

    	if (options.fpack is None) and  (not options.list ):
    	    print >> sys.stderr, "provide name for feature pack"
    	    sys.exit(1)
    	if (options.skuname is None) and  (not options.list ):
    	    print >> sys.stderr, "provide the sku name, run -s to get sku list"
    	    sys.exit(1)

	skuname=options.skuname
	fpack=options.fpack

	featurejson={
	"stm_sku": skuname, 
	"excluded": ""
	}
	if not options.list:
		addFeature(featurejson,fpack)
	

if __name__ == "__main__":
    main()
