
#Authors: Thomas Meisel and Lauren Buck
#Date Created: September 27,2015
#Created for CS5287: Cloud Computing
#Institution Vanderbilt University

import time
import BaseHTTPServer
import prime
import nova_server_create

HOST = ''
PORT = 8080
total_time = 0
num = 0
vm_array = []

# MyHTTPHandler inherits from BaseHTTPServer.BaseHTTPRequestHandler
class MyHTTPHandler (BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET (self):
        global total_time
        global num
        global vm_array
        """ Respond to a GET request. """
        print "GET request received; reading the request"
        #do is_prime from the vm 
        is_prime, processing_time = prime.is_prime(int(self.path[1:]))
        num += 1
        total_time += processing_time 
        average_time = total_time/num 
        #if average_time is greater than certain amount, spawn new vm
        if average_time > 1 :
            add_vm(vm_array)
        #if average_time is less than certain amount, terminate vm
        if average_time < .0001 and len(vm_array) > 1 :
            remove_vm(vm_array)
        #terminate function in httpclient2.py still to be completed
        print "Received request = ", self 
        self.send_response (200)
        self.send_header ("Content-type", "text/html")
        self.end_headers ()
        self.wfile.write ("<html><head><title>Title</title></head>")
        self.wfile.write ("<body><p>Is Prime: %s</p>" % is_prime)
        self.wfile.write ("<p>Processing Time: %s</p>" % processing_time)
        self.wfile.write ("<p>Number of Requests: %s</p>" % num)
        self.wfile.write ("<p>Average Processing Time: %s</p>" % average_time) 
        self.wfile.write ("</body></html>")

def add_vm (vms):
    #comment out the next two lines when debugging
    server = nova_server_create.create_vm()
    vms.append(server)
    #uncomment the next line when not debugging
    #vms.append("VM0")
    print "VM created"
    print "Number of VMs: %s" % len(vms)

def remove_vm (vms):
    #comment out the next line when debugging
    nova_server_create.terminate_vm(vms.index(0))
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


