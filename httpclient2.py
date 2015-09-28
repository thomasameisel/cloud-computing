
#Authors: Lauren Buck and Thomas Meisel
#Date Created: September 28, 2015
#Created for CS5287: Cloud Computing
#Institution: Vanderbilt University

#Starts virtual machine to handle requests sent to server. Additionally, invokes look busy on the
#virtual machine to simulate busy load. As response times slow, allocates a new virtual machine
#to handle incoming tasks via a (a) round robin or (b) priority method.

import os
import sys
import httplib
import time
from novaclient.v2 import client

def get_nova_creds():
    d={}
    d['version'] = '2'
    d['username'] = os.environ['OS_USERNAME']
    d['api_key'] = os.environ['OS_PASSWORD']
    d['auth_url'] = os.environ['OS_TENANT_NAME']
    return d

def main():
    #Retrieve credentials for version 2 of novaclient
    creds = get_nova_creds()

    #Access the connection from which everything else is obtained
    try:
        nova = client.Client(**creds)
    except:
        print "Exception thrown, " sys.exc_info()[0]
        raise

    #Retrieve underlying references for various attributes
    imageref = nova.images.find(name="ubuntu-14.04")
    flavorref = nova.flavors.find(name="m1.small")
    sgref = nova.security_groups.find(name="default")

    attrs = {
        'name' : 'test_vm',
        'image': imageref,
        'flavor' : flavorref,
        'key_name' : 'buck',
        'nics' : [{'net-id' : 'b16b0244-e1b5-4d36-90ff-83a0d87d8682'}]
    }

    try:
        server = nova.servers.create(**attrs)
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        raise

    #Check to see if server is up:
    while(server.status != 'ACTIVE'):
        print "Not active yet; sleep for a while."
        time.sleep(2)
        server = nova.servers.find(name='test_vm')

    #Add a floating IP
    try:
        #Associates a floating IP with the server
        server.floating_ip_create('ext-net')
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        server.delete()
        raise

#Invoke Main:
if __name__ == "__main__":
    main()