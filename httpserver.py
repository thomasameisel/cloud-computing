# !/bin/python
import time
import BaseHTTPServer
import prime

HOST = ''
PORT = 8080
total_time = 0
num = 0

# MyHTTPHandler inherits from BaseHTTPServer.BaseHTTPRequestHandler
class MyHTTPHandler (BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET (self):
        global total_time
        global num 
        """ Respond to a GET request. """
        print "GET request received; reading the request"
        is_prime, processing_time = prime.is_prime(int(self.path[1:]))
        num += 1
        total_time += processing_time 
        average_time = total_time/num 
        print "Received request = ", self 
        self.send_response (200)
        self.send_header ("Content-type", "text/html")
        self.end_headers ()
        self.wfile.write ("<html><head><title>Title</title></head>")
        self.wfile.write ("<body><p>Is Prime: %s</p>" % is_prime)
        self.wfile.write ("<p>Processing Time: %s</p>" % processing_time)
        self.wfile.write ("<p>Number of Requests: %s</p>" % num)
        self.wfile.write ("<p>Average Processing Time: %s</p>" % average_time) 
        self.wfile.write ("</body.<html>")


if __name__ == '__main__':
    print "Instantiating a BaseHTTPServer"
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class ((HOST, PORT), MyHTTPHandler)
    try:
        print "Run a BaseHTTPServer"
        httpd.serve_forever ()
    except KeyboardInterrupt:
        pass

    httpd.server_close ()


