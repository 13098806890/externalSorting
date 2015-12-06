__author__ = 'Teemo'
import os
import time
from random import Random

def getRandomString(stringlength):
    sourceString = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+-*/='
    sourceString_len = len(sourceString)
    str = ''
    random = Random()
    for i in range(stringlength):
        str += sourceString[random.randint(0,sourceString_len-1)]
    return str

def getRandomString1(stringlength):
    sourceString = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+-*/='
    sourceString_len = len(sourceString)
    str = ''
    random = Random()
    for i in range(stringlength):
        str += random.choice(sourceString)
    return str

def getRandomString3(stringlength):
    sourceString = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+-*/='
    # sourceString = ['1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','+','-','*','/','=']
    sourceString_len = len(sourceString)
    random = Random()
    TMstr = ''.join(random.sample(sourceString,stringlength))
    return str

def testForLoop():
    number = 0
    for i in range(1000):
        for j in range(1000):
            for k in range(1000):
                number += k



startTime = time.time()
testForLoop()
endTime = time.time()
print(str(endTime - startTime))