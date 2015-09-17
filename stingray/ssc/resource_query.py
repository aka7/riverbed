#! /usr/bin/env python  
# to change ssc manager settings.

import requests  
import json  
import sys,os  
import ssc_common
from optparse import OptionParser
from ssc_common import getSSCURI,getPassword,sscConnection,listurl,showResource,listResource


# provide FQDN stm name to be created as non-managed on ssc 
# set license keyi and bandwidth for this stm
def main():
    parser = OptionParser(version='0.1')
    parser.add_option("--debug", dest="debug",
        default=False,
        help="Show debugging")

    parser.add_option("-n", "--notreally", dest="not_really",
        default=False,
        help="Don't create anything")
    parser.add_option("-s", "--show", dest="show",
        default=None,
        help="list resources")
    parser.add_option("-q", "--query", dest="query",
        default=None,
        help="show detailed resources object")
    parser.add_option("-u", "--username", dest="username",
        default=None,
        help="username for api access")

    (options, args) = parser.parse_args()
    if options.debug:
        global debug
        debug = True

    username='sscadmin'
    if not options.username is None:
	username = options.username
    ssc_common.username=username
    if options.show:
	listResource(options.show)
        sys.exit(0)

    if not options.query is None:
	showResource(options.query)
        sys.exit(0)
	
if __name__ == "__main__":
    main()

