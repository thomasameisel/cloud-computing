#!/bin/python
#
# sample http client
#
import requests
import thread
import time
from random import randint

def main ():

    params = {'num':randint(1000000000000000,10000000000000000)}
    r = requests.get("http://localhost:8080", params)
    print r.json()

# invoke main
if __name__ == "__main__":
    while True: 
        thread.start_new_thread(main, ())
        time.sleep(0.1)