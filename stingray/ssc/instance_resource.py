#! /usr/bin/env python  
# adding a stm instance to ssc controller as non-managed
# once added, you need to install the FLA key on the instance.
import requests  
import json
import ssc_common
import sys,os,getpass
from optparse import OptionParser
from ssc_common import getPassword,sscConnection,listurl,showResource,getSSCURI, printjson, showBW

# Following environment var needs to be set.
# get ssc admin pass from environment, assumes admin
# get stm admin password, defaults to admin, can be changed later

# TODO: lot more improvement
  
def addHost(stmName):
# adds instacne in host resource, its needed.
	
	hostjson={"install_root": "/data/stminstall", "work_location": "/var/cache/ssc", "username": "root"}
	uri=getSSCURI()
	url = uri+'host/'+stmName
	jsontype = {'content-type': 'application/json'}  

	client = sscConnection()  
	  
	try:  
    	#First see if the host entry already exists  
	    response = client.get(url)  
	except requests.exceptions.ConnectionError:  
	    print "Error: Unable to connect to " + url  
	    sys.exit(1) 
	
	if (response.status_code == 401):  
		print response.content
	        sys.exit(1)  
		
	
	if (response.status_code == 404):  
	    response = client.put(url, data = json.dumps(hostjson), headers = jsontype)  
	    if response.status_code == 201: # When creating a new resource we expect to get a 201  
	        print 'host resource for stm %s added' %(stmName) 
		print response.content
	    else:  
	        data = json.loads(response.content)  
	        print "Error adding host resource %s: URL=%s Status=%d Id=%s: %s" %(stmName, url, response.status_code, data['error_id'], data['error_info'])  
	else:  
	    if response.status_code == 200:  
	        print "host resource  %s already exists, continue creating instance" %(stmName) 
	    else:  
	        print "Error: Status=%d URL=%s" %(response.status_code, url)    


def addInstance(stmName,instancejson, updatejson):
	# need a entry for this non-maanaged hsot in host resource.
	addHost(stmName)
	uri=getSSCURI()
	url = uri+'instance/'+stmName+'?managed=false'
	jsontype = {'content-type': 'application/json'}  
  
	client = sscConnection()  
	try:  
	    #First see if the stm already exists  
	    response = client.get(url)  
	except requests.exceptions.ConnectionError:  
	    print "Error: Unable to connect to " + url  
	    sys.exit(1)  
	
	if (response.status_code == 404):  
	    response = client.put(url, data = json.dumps(instancejson), headers = jsontype)  
	    if response.status_code == 201: # When creating a new resource we expect to get a 201  
	        print 'instance resource for %s added' %(stmName)  
		print response.content
	    else:  
	        data = json.loads(response.content)  
	        print "Error adding instance %s: URL=%s Status=%d Id=%s: %s" %(stmName, url, response.status_code, data['error_id'], data['error_info'])  
	else:  
	    if response.status_code == 200:  
	        print "instance resource %s already exists, updating" %(stmName)  
	    	response = client.put(url, data = json.dumps(updatejson), headers = jsontype)  
	    	if response.status_code == 200: # When update a new resource we expect to get a 200
			print 'instance resource %s updated' %(stmName)  
			printjson(response.content)
	    	elif response.status_code == 400: # when its already delete / inactive expect 400, you cannot update a delete instance
	    		print 'stm %s deleted or inactive cannot udpate a deleted instance' %(stmName)  
			printjson(response.content)
	    	    	data = json.loads(response.content)  
	        	print "Error adding instance %s: URL=%s Status=%d Id=%s: %s" %(stmName, url, response.status_code, data['error_id'], data['error_text'])  
	    	else:  
	    	    	data = json.loads(response.content)  
	        	print "Error adding instance %s: URL=%s Status=%d Id=%s: %s" %(stmName, url, response.status_code, data['error_id'], data['error_info'])  
	    else:  
	        print "Error: Status=%d URL=%s" %(response.status_code, url)    

def changeInstanceStatus (stmName,status):
	updateinstance={
		"status": status,
	}

	uri=getSSCURI()
	url = uri+'instance/'+stmName
	jsontype = {'content-type': 'application/json'}  
	client = sscConnection()  
	try:  
	    #First see if the stm already exists  
	    response = client.get(url)  
	except requests.exceptions.ConnectionError:  
	    print "Error: Unable to connect to " + url  
	    sys.exit(1)  
	if (response.status_code == 404):  
	    print 'stm %s does not exist' %(stmName)  
	else:  
	    if response.status_code == 200:  
	        print "stm %s exists"  %(stmName)  
		print "action "+status
	    	response = client.put(url, data = json.dumps(updateinstance), headers = jsontype)  
	    	if response.status_code == 200: # When updating a new resource we expect to get a 200
			print 'stm %s status changed' %(stmName)  
			print response.content
	    	elif response.status_code == 400: # when its already delete inactive expect 400 
	    	    	data = json.loads(response.content)  
	        	print "Error changing status of instance %s: URL=%s Status=%d Id=%s: %s" %(stmName, url, response.status_code, data['error_id'], data['error_text'])  
	    	else:  
	    	    	data = json.loads(response.content)  
	        	print "Error changing status of instance %s: URL=%s Status=%d Id=%s: %s" %(stmName, url, response.status_code, data['error_id'], data['error_info'])  
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

    parser.add_option("-i", "--instance", dest="instancename",
        default=None,
        help="hostname to add to sssc")
    parser.add_option("-l", "--lic", dest="license",
        default=None,
        help="fla license for the instance")
    parser.add_option("-b", "--bandwidth", dest="bandwidth",
        default=None,
        help="bandwidth allocation for the instance")
    parser.add_option("--show-bandwidth", dest='showbw',
	action="store_true", default=False,
        help="show all allocated bandwidth")
    parser.add_option("-u", "--username", dest="username",
        default=None,
        help="username for api access")
    parser.add_option("-f", "--fpack", dest="fpack",
        default=None,
        help="feature pack")
    parser.add_option("-r", "--remove", dest="remove",
        action="store_true",default=False,
        help="delete a given instance")
    parser.add_option("-c", "--change", dest="changestatus",
        default=None,
        help="change instance status to active, Active/Idle")
    parser.add_option("-s", "--show", dest="show",
        action="store_true",default=False,
        help="list all current instance resouce")
    parser.add_option("-q", "--query", dest="query",
        default=None,
        help="list resource of a given instance")
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
    	listurl('instance')
        sys.exit(0)

    if not options.query is None:
	showResource(options.query)
        sys.exit(0)

    if options.showbw:
	showBW()
        sys.exit(0)
	
    if (options.instancename is None) and  (not options.show ):
        print >> sys.stderr, "Provide instancename"
        sys.exit(1)

    stmName=options.instancename

    if options.remove:
    	changeInstanceStatus(stmName,"Deleted")
        sys.exit(0)
    if  not options.changestatus is None:
    	changeInstanceStatus(stmName,options.changestatus)
        sys.exit(0)

   # default values, can be changed later
    license ='STM_684893_License.fla'
    admin_password='admin'
    fpack= 'STM-U-CSP-400-FP' 


    # json object for creating a new instance, setting default values as defined above.
    instancejson={
    "config_options": "",
    "stm_version" : "9.4", 
    "rest_address": stmName+":9070", 
    "snmp_address": stmName+":161", 
    "admin_username": username, 
    "cpu_usage": "0",
    "stm_feature_pack": fpack, 
    "ui_address": stmName+":9090", 
    "container_configuration": "", 
    "admin_password": admin_password,
    "owner": "websys", 
    "license_name" : license,
    "management_address": stmName,
    "host_name": stmName}

    # construct json object to to update an instacne, only update what we need to update, provided from cmdline, when empty nothing will change
    updateinstancejson={}

    if options.adminpass:
	admin_password=getPassword('stminstance','Enter instance admin password for rest api: ')
    	updateinstancejson["admin_password"] = admin_password
    	instancejson["admin_password"] = admin_password

    if not options.license is None:
    	license =options.license
    	updateinstancejson["license_name"] = license
    	instancejson["license_name"] = license
    if not options.username is None:
    	username =options.username
    	updateinstancejson["admin_username"] = username
    	instancejson["admin_username"] = username
    if not options.bandwidth is None:
    	bandwidth =int(options.bandwidth)
    	updateinstancejson["bandwidth"] = bandwidth 
    	instancejson["bandwidth"] = bandwidth 
    if not options.fpack is None:
  	fpack =options.fpack
    	updateinstancejson["stm_feature_pack"] = fpack
    	instancejson["stm_feature_pack"] = fpack

    if not options.show:
    	addInstance(stmName,instancejson, updateinstancejson)

if __name__ == "__main__":
    main()

