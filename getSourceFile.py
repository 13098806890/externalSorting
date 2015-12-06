__author__ = 'Teemo'
import os
import time
from random import Random
dir = '/Users/Teemo/datasFile/'
sourceFile = 'sourceData'


def getRandomString(stringlength):
    sourceString = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+-*/='
    sourceString_len = len(sourceString)
    str = ''
    random = Random()
    for i in range(stringlength):
        str += sourceString[random.randint(0,sourceString_len-1)]
    return str

outPutPath = dir + sourceFile
# os.remove(outPutPath)
outPutFile = open(outPutPath,'a')
if not os.path.exists(dir):
    os.mkdir(dir)
for i in range(2000):#4G
    startTime = time.time()
    for j in range(90):#1M
        tempStr = ''
        for k in range(500):#64k
            tempStr += getRandomString(20)+'\r\n'
        outPutFile.write(tempStr)
        outPutFile.flush()
    endTime = time.time()
    duration = endTime - startTime
    print(str(i+1) + 'M     cost time : '+ str(duration) + '\r\n')

outPutFile.close()
