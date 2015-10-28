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
    r = requests.get("http://10.10.1.38:8080", params=params)
    return r.json()

# invoke main
if __name__ == "__main__":
    for num in range(1, 5):
	num = 101010101101
	data = main(num)
        print "Num: %s Time: %s Average: %s" % (101, data["processing_time"], data["average_processing_time"])
	time.sleep(45)
    for num in range(1, 3):
	num = 1010101011011111
	data = main(num)
        print "Num: %s Time: %s Average: %s" % (num, data["processing_time"], data["average_processing_time"])
	time.sleep(45)
    for num in range(1, 10):
	num = 101010101101
	data = main(num)
	print "Num: %s Time: %s Average: %s" % (101, data["processing_time"], data["average_processing_time"])
        time.sleep(45)
