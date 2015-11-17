#!/bin/python
#
# sample http client
#
import sys
import httplib
import getopt

use_primary = True

def main (argv):
    global use_primary

    primary = ""
    backup = ""
    server = ""

    try:
        opts, args = getopt.getopt(argv, "",["primary=","backup="])
    except getopt.GetoptError:
        print "Server IPs not specified"
        raise

    for opt, arg in opts:
        if opt in ("--primary"):
            primary = arg
        elif opt in ("--backup"):
            backup = arg

    if use_primary:
        print "Using primary server"
        server = primary
    else:
        print "Using backup server"
        server = backup

    try:
        conn = httplib.HTTPConnection (server, "8080")
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        raise

    print "sending a GET request to %s server" % server
    try:
        conn.request ("GET", "/")
    except:
        if use_primary:
            print "Switching to backup"
            use_primary = False
            return
        else:
            print "Exception thrown: ", sys.exc_info()[0]
            raise

    print "retrieving a response from %s server" % server
    try:
        resp = conn.getresponse ()
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        raise

# invoke main
if __name__ == "__main__":
    while True:
        main(sys.argv[1:])
    
