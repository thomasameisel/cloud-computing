
#Authors: Thomas Meisel and Lauren Buck
#Date Created: September 27,2015
#Created for CS5287: Cloud Computing
#Institution Vanderbilt University

import BaseHTTPServer
import time
import urlparse
import json

HOST = ''
PORT = 8080
total_time = 0
num_requests = 0
vm_array = []

# MyHTTPHandler inherits from BaseHTTPServer.BaseHTTPRequestHandler
class MyHTTPHandler (BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET (self):
        global PORT
        """ Respond to a GET request. """
        print "GET request received; reading the request"
        parsed = urlparse.urlparse(self.path)
        prime_num = (urlparse.parse_qs(parsed.query)['num'])[0]
        is_prime, processing_time = self.is_prime(int(prime_num))
        response = {"is_prime":is_prime, "processing_time":processing_time}
        self.send_response (200)
        self.send_header ("Content-type", "application/json")
        self.end_headers ()
        self.wfile.write(json.dumps(response))

    def is_prime(self,num):

        a = True
        b = True
        c = True

        t1 = time.clock()

        if  num <= 1:
            #print('This is NOT a prime number.')
            a = False;
        elif num % 2 == 0 or num % 3 == 0:
            #print('This is NOT a prime number.')
            b = False;
        else:
            i = 5
            while i*i <= num:
                if num % i == 0 or num % (i + 2) == 0:
                    #print('This is NOT a prime number.')
                    c = False;
                i = i + 6

        t2 = time.clock()
        processing_time = t2-t1

        if a != False and b != False and c != False:
            return (True, processing_time)
        else:
            return (False, processing_time)

if __name__ == '__main__':
    #print "Instantiating a Prime BaseHTTPServer"
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class ((HOST, PORT), MyHTTPHandler)
    try:
        #print "Run a Prime BaseHTTPServer"
        httpd.serve_forever ()
    except KeyboardInterrupt:
        pass

    httpd.server_close ()


