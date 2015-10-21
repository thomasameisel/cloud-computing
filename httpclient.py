#!/bin/python
#
# sample http client
#
import requests
import thread
import time
from random import randint

def main (num):

    params = {'num':num}
    r = requests.get("http://10.10.1.123:8080", params=params)
    return r.json()

# invoke main
if __name__ == "__main__":
    for num in range(1, 5):
	num = 101
	data = main(num)
        print "Num: %s Time: %s" % (101, data["processing_time"])
    while True:
	num = 101010101101
	data = main(num)
        print "Num: %s Time: %s" % (num, data["processing_time"])
