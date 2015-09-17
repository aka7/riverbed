#! /usr/bin/env python  
# common modules for ssc api, shared DF
# like a config file, but in module
# NOTE: set your sscva address here.
# sscadm user, etc here.

import requests  
import json  
import sys,os,getpass
from sscuser import sscuser
from optparse import OptionParser

# Following environment var needs to be set.
# get ssc admin pass from environment, assumes admin
# get stm admin password, defaults to admin, can be changed later

# if updating existing instance, management_address, host_name and owner can't not be updated.

ssc_ver = '1.0'
username = 'sscadmin'

def sscConnection():
	username = getUsername() 
	ssc_pass=getPassword(username,'Enter password for user ' + username +' : ')
	client = requests.Session()
        client.auth = (username, ssc_pass)
        client.verify = False
	return client

def readRCFile(username):
	hpath=os.path.expanduser('~')
	rcfile=hpath+'/.sscrc'
	if os.path.exists(rcfile):
		configfile = open(rcfile,'r')
		for line in configfile.readlines():
			if line.startswith('#'):
				pass
			else:
				key,value= line.split(':')
				if key == username:
					return value
	return ""
	

def getPassword(username,outstring):
	password = readRCFile(username)
	if password == "":
		password=getpass.getpass(outstring)
	return password.strip()
def getUsername():
	return username 


def getSSCHost():
	#set your ssc address
	return 'sscva.yourdomain.com'

def getSSCPort():
# set this to your port
	return '8000'

def getSSCURI():
	host=getSSCHost()
	port=getSSCPort()
	return 'https://'+host+':'+port+'/api/tmcm/'+ssc_ver+'/'

def listurl(name):
	uri=getSSCURI()
	url = uri+name
	jsontype = {'content-type': 'application/json'}  
	  
	client = sscConnection()  
	  
	try:  
	    response = client.get(url)  
	except requests.exceptions.ConnectionError:  
	    print "Error: Unable to connect to " + url  
	    sys.exit(1)  

	if (response.status_code == 401):  
		# access denied to ssc game over
		print response.content
	        sys.exit(1)  
	
	if (response.status_code == 404):  
	    print 'resource does not exist %s'
	else:  
	    if response.status_code == 200:  
		#print response.content
		data = json.loads(response.content)
		for key,value in data.iteritems():
			for i in range(len(value)):
				print value[i]['href']
			
	    else:  
	        print "Error: Status=%d URL=%s" %(response.status_code, url)    

def listResource(href):
	host=getSSCHost()
	port=getSSCPort()
	url = 'https://'+host+':'+port+href
	jsontype = {'content-type': 'application/json'}  
	  
	client = sscConnection()  
	  
	try:  
	    response = client.get(url)  
	except requests.exceptions.ConnectionError:  
	    print "Error: Unable to connect to " + url  
	    sys.exit(1)  

	if (response.status_code == 401):  
		# access denied to ssc game over
		print response.content
	        sys.exit(1)  
	
	if (response.status_code == 404):  
	    print 'resource does not exist %s'
	else:  
	    if response.status_code == 200:  
		#print response.content
		data = json.loads(response.content)
		for key,value in data.iteritems():
			for i in range(len(value)):
				print value[i]['href']
			
	    else:  
	        print "Error: Status=%d URL=%s" %(response.status_code, url)    

def showResource(href):
	host=getSSCHost()
	port=getSSCPort()
	url = 'https://'+host+':'+port+href
	jsontype = {'content-type': 'application/json'}  
	  
	client = sscConnection()  
	  
	try:  
    	#First see if the host entry already exists  
	    response = client.get(url)  
	except requests.exceptions.ConnectionError:  
	    print "Error: Unable to connect to " + url  
	    sys.exit(1)  
	
	if (response.status_code == 404):  
	    print 'resource does not exist %s'
	else:  
	    if response.status_code == 200:  
		#printjson(response.content)
		print response.content
			
	    else:  
	        print "Error: Status=%d URL=%s" %(response.status_code, url)    

def getBW(href):
# get bandwidth of a given instance
	host=getSSCHost()
	port=getSSCPort()
	url = 'https://'+host+':'+port+href
	jsontype = {'content-type': 'application/json'}  
	  
	client = sscConnection()  
	  
	try:  
    	#First see if the host entry already exists  
	    response = client.get(url)  
	except requests.exceptions.ConnectionError:  
	    print "Error: Unable to connect to " + url  
	    sys.exit(1)  
	
	if (response.status_code == 404):  
	    print 'resource does not exist %s'
	    return 0
	else:  
	    if response.status_code == 200:  
		instance = json.loads(response.content)
		print "[ ", instance['status'], " ]",
		if instance['status'] == 'Deleted':
			return 0
		else:
			return instance['bandwidth']
	    else:  
	        print "Error: Status=%d URL=%s" %(response.status_code, url)    
	return 0

def showBW():
# show badnwidth of each instance
	host=getSSCHost()
	port=getSSCPort()
	href="/api/tmcm/"+ssc_ver+"/instance"
	url = 'https://'+host+':'+port+href
	jsontype = {'content-type': 'application/json'}  
	totalbw=0
	  
	client = sscConnection()  
	  
	try:  
	    response = client.get(url)  
	except requests.exceptions.ConnectionError:  
	    print "Error: Unable to connect to " + url  
	    sys.exit(1)  

	if (response.status_code == 401):  
		# access denied to ssc game over
		print response.content
	        sys.exit(1)  
	
	if (response.status_code == 404):  
	    print 'resource does not exist %s'
	else:  
	    if response.status_code == 200:  
		data = json.loads(response.content)
		for key,value in data.iteritems():
			for i in range(len(value)):
			     bw=getBW(value[i]['href'])
			     print value[i]['name']+" : ", bw
			     totalbw+=bw
	    else:  
	        print "Error: Status=%d URL=%s" %(response.status_code, url)    
	print "Total BW allocation: ",totalbw
	if totalbw > 5000:
		print "WARN: over allocated bandwidth in cluster"

def printjson(jsoncontent):
	data = json.loads(jsoncontent)
	for key,value in data.iteritems():
		print key,' : ',value
