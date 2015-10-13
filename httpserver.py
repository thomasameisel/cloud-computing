
#Authors: Thomas Meisel and Lauren Buck
#Date Created: September 27,2015
#Created for CS5287: Cloud Computing
#Institution Vanderbilt University

import json
import BaseHTTPServer
import nova_server_create
import requests
import urlparse
import primeserver
import thread
from commands import *

HOST = ''
PORT = 8080
total_time = 0
num_requests = 0
round_robin = True
vm_array = []
vm_cur_index = 0

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

        #later this will be the server to use, now it is just the next port to use for the local server
        next_vm = choose_vm(vm_array)
        params = {'num':prime_num,'response_num':num_requests+1}
        r = requests.get("http://%s:8080"%(next_vm.addresses)['internal network'][0]['addr'],params=params)
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

#later this will create a new server
#since creating new servers is not working, it creates a new server locally on a new port
def add_vm (vms):
    #comment out the next two lines when debugging
    server = nova_server_create.create_vm()
    #not sure how to get the fixed ip of the server
    ip_address = (server.addresses)['internal network'][0]['addr']
    getstatusoutput('scp -i key_pair2.pem -o StrictHostKeyChecking=no primeserver.py ubuntu@%s:/home/ubuntu;ssh -i key_pair2.pem -o StrictHostKeyChecking=no ubuntu@%s "nohup python primeserver.py > /dev/null 2>&1 &"'%(ip_address,ip_address))
    vms.append(server)
    #uncomment the next lines when not debugging
    #global vm_cur_port
    #thread.start_new_thread(primeserver.create_instance, ("",vm_cur_port))
    #vms.append(vm_cur_port)
    #vm_cur_port += 1
    print "VM created"
    print "Number of VMs: %s" % len(vms)

#later this will terminate a server
def remove_vm (vms):
    #comment out the next line when debugging
    nova_server_create.terminate_vm(vms.index(0))
    vms.pop(0)
    print "VM terminated"
    print "Number of VMs: %s" % len(vms)

#later this will choose the create vm
#since creating new vms is not working, it returns the port of the next vm
def choose_vm (vms):
    global round_robin
    global vm_cur_index
    if round_robin:
        vm_cur_index = (vm_cur_index+1) % len(vms)

    return vms[vm_cur_index]

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
    
    for server in vm_array:
        nova_server_create.terminate_vm(server)

    httpd.server_close ()


