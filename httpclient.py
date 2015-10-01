#!/bin/python
#
# sample http client
#
import requests
import time

def main ():
    params = {'num':'123422342323423'}
    r = requests.get("http://localhost:8080", params)
    print r.json()

# invoke main
if __name__ == "__main__":
    while True: 
        main ()
        time.sleep(2)
    
