__author__ = 'Teemo'
import os


line_feed = '\r\n'

def getLinesFromFile(filePath):
    if os.path.exists(filePath):
        file = open(filePath,'r')
        lines = file.readlines()
        file.close()
        return lines
    else:
        print(filePath + 'does not exist.')

def getFileNamesFromFolder(filePath,postfix = None):
    def filterWithPostfix(fileName):
        if fileName[0] == '.':
            return False
        elif postfix != None:
            if fileName.split('.')[-1] != postfix:
                return False
            else:
                return True
        elif postfix == None:
            if len(fileName.split('.')) > 1:
                return False
            else:
                return True
        else:
            return True

    if os.path.exists(filePath):
        fileNames = os.listdir(filePath)
        return filter(filterWithPostfix,fileNames)
    else:
        print filePath + 'does not exist.'

def writeLines(dstPath,lines):
    try :
        with open(dstPath, "w") as file:
            file.writelines(lines)
            file.close()
    except IOError as err:
            print(err)