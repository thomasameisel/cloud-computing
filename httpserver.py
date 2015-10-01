
#Authors: Thomas Meisel and Lauren Buck
#Date Created: September 27,2015
#Created for CS5287: Cloud Computing
#Institution Vanderbilt University
import json

import time
import BaseHTTPServer
import prime
import nova_server_create
import httplib
import requests
import urlparse

HOST = ''
PORT = 8080
total_time = 0
num_requests = 0
vm_array = []

# MyHTTPHandler inherits from BaseHTTPServer.BaseHTTPRequestHandler
class MyHTTPHandler (BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET (self):
        global total_time
        global num_requests
        global vm_array

        """ Respond to a GET request. """
        print "GET request received; reading the request"
        parsed = urlparse.urlparse(self.path)
        prime_num = (urlparse.parse_qs(parsed.query)['num'])[0]

        params = {'num':prime_num }
        r = requests.get("http://localhost:8000",params)
        data = r.json()
        is_prime = data["is_prime"]
        processing_time = data["processing_time"]

        num_requests += 1
        total_time += processing_time
        average_time = total_time/num_requests
        #if average_time is greater than certain amount, spawn new vm
        if average_time > 1 :
            add_vm(vm_array)
        #if average_time is less than certain amount, terminate vm
        if average_time < .0001 and len(vm_array) > 1 :
            remove_vm(vm_array)

        response = {"number":prime_num, "is_prime":is_prime, "processing_time":processing_time,
                    "num_requests":num_requests, "average_processing_time":average_time}

        self.send_response (200)
        self.send_header ("Content-type", "application/json")
        self.end_headers ()
        self.wfile.write (json.dumps(response))

def add_vm (vms):
    #comment out the next two lines when debugging
    #server = nova_server_create.create_vm()
    #vms.append(server)
    #uncomment the next line when not debugging
    vms.append("VM0")
    print "VM created"
    print "Number of VMs: %s" % len(vms)

def remove_vm (vms):
    #comment out the next line when debugging
    #nova_server_create.terminate_vm(vms.index(0))
    vms.pop(0)
    print "VM terminated"
    print "Number of VMs: %s" % len(vms)

if __name__ == '__main__':
    print "Instantiating a BaseHTTPServer"
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class ((HOST, PORT), MyHTTPHandler)
    add_vm(vm_array)
    try:
        print "Run a BaseHTTPServer"
        httpd.serve_forever ()
    except KeyboardInterrupt:
        pass

    httpd.server_close ()


