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
    for num in range(1, 2):
	num = 101010101101
	data = main(num)
	print data
	time.sleep(5)
    for num in range(1, 3):
	num = 1010101011011111
	data = main(num)
	print data
	time.sleep(60)
    for num in range(1, 10):
	num = 101010101101
	data = main(num)
        print data
	time.sleep(15)
