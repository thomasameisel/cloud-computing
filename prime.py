
import math

#Author: Lauren E Buck
#Created: September 21, 2015
#Institution: Vanderbilt University

#Code takes in a number and checks to see if that number is prime.

#Input here needs to be grabbed from the browser...
num = input('Enter a number: ')

def is_prime(num):
    
    a = True
    b = True
    c = True
    
    if  num <= 1:
        print('This is NOT a prime number.')
        a = False;
    elif num <= 3:
        print('This is a prime number.')
    elif num % 2 == 0 or num % 3 == 0:
        print('This is NOT a prime number.')
        b = False;
    i = 5
    while i*i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            print('This is NOT a prime number.')
            c = False;
        i = i + 6

    if a != False and b != False and c != False:
        print('This is a prime number.')

#Function call
is_prime(num)