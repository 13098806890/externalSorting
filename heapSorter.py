__author__ = 'Teemo'
import os
import tm_com
import time
import someOldCodes


#class
from abc import ABCMeta, abstractmethod
from abc import abstractproperty

class tm_HeapSortable():
    __metaclass__ = ABCMeta

    def __init__(self,values):
        if isinstance(values,list):
            self.dataList = values
            self.size = len(values)
        else:
            print("values : " + str(values))
            print ("init failed, the 'values' you passed is not a list.")

    def dataList(self):
        return self.dataList

    def size(self):
        return self.size

    def leftChlidIndex(self,index):
        return 2 * index + 1

    def rightChildIndex(self,index):
        return 2 * index + 2

    def leftChild(self,index):
        return self.dataList[2 * index + 1]

    def rightChild(self,index):
        return self.dataList[2 * index + 2]

    def hasRightChild(self,position,endIndex):
        if endIndex >= position * 2 + 2:
            return True
        else:
            return False

    def hasLeftChild(self,position,endIndex):
        if endIndex >= position * 2 + 1:
            return True
        else:
            return False

    def getLastParentNodeIndex(self,endIndex):
        return (endIndex - 1)/2

    @abstractmethod
    def exchangeValue(self,toIndex,fromIndex):
        pass

    @abstractmethod
    def cmpValue_moreThan(self,index1,index2):
        pass

    @abstractmethod
    def cmpValue_lessThan(self,index1,index2):
        pass

    @abstractmethod
    def write(self):
        pass

    @abstractmethod
    def __lt__(self, other):
        pass

    @abstractmethod
    def __le__(self, other):
        pass

    @abstractmethod
    def __gt__(self, other):
        pass

    @abstractmethod
    def __ge__(self, other):
        pass

    @abstractmethod
    def __ne__(self, other):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass


class tm_SimpleDataList(tm_HeapSortable):

    def exchangeValue(self,toIndex,fromIndex):
        temp = self.dataList[fromIndex]
        self.dataList[fromIndex] = self.dataList[toIndex]
        self.dataList[toIndex] = temp

    def cmpValue_moreThan(self,index1,index2):
        if self.dataList[index1] > self.dataList[index2]:
            return True
        else:
            return False

    def cmpValue_lessThan(self,index1,index2):
        return not self.cmpValue_moreThan(index1,index2)

    def write(self):
        pass

class tm_SingleFile(tm_SimpleDataList):

    def __init__(self,filePath):
        self.filePath = filePath
        lines = tm_com.getLinesFromFile(filePath)
        self.name = filePath
        super(tm_SimpleDataList,self).__init__(lines)

    def write(self):
        tm_com.writeLines(self.filePath,self.dataList)
        print 'write done : ' + self.name

class tm_DividedFile():
    def __init__(self,filePath):
        self.filePath = filePath
        self.lines = tm_com.getLinesFromFile(self.filePath)
        self.size = len(self.lines)
        self.start = self.lines[0]
        self.end = self.lines[-1]

class tm_FileDataList(tm_HeapSortable):

    def exchangeValue(self,toIndex,fromIndex):
        toIndexFileSize = self.dataList[toIndex].size
        fromIndexFileSize = self.dataList[fromIndex].size
        if toIndexFileSize > fromIndexFileSize:
            biggerSize = toIndexFileSize
            litterSize = fromIndexFileSize
        else:
            biggerSize = fromIndexFileSize
            litterSize = toIndexFileSize
        allLines = []
        if self.dataList[toIndex].end > self.dataList[fromIndex].start:
            tempFilePath = self.dataList[fromIndex].filePath + 'temp'
            os.rename(self.dataList[fromIndex].filePath,tempFilePath)
            os.rename(self.dataList[toIndex].filePath,self.dataList[fromIndex].filePath)
            os.rename(tempFilePath,self.dataList[toIndex].filePath)
        else:
            i = 0
            j = 0
            while i < self.dataList[fromIndex].size and j < self.dataList[toIndex]:
                if self.dataList[fromIndex].lines[i] < self.dataList[toIndex].lines[j]:
                    allLines.append(self.dataList[fromIndex].lines[i])
                    i += 1
                else:
                    allLines.append(self.dataList[toIndex].lines[j])
                    j += 1
            if i < self.dataList[fromIndex]:
                allLines.append(self.dataList[fromIndex].lines[i:])
            else:
                allLines.append(self.dataList[toIndex].lines[j:])

    def cmpValue_moreThan(self,index1,index2):
        if self.dataList[index1].start < self.dataList[index2].start:
            return True
        else:
            return False

    def cmpValue_lessThan(self,index1,index2):
        return not self.cmpValue_moreThan(index1,index2)
    def write(self):
        pass

class tm_HeapSorter():

    def __init__(self,heapSortableObj):
        if isinstance(heapSortableObj,tm_HeapSortable):
            self.heapSortableObj = heapSortableObj
        else:
            print('the value you pass id not a subclass of tm_HeaoSortable.')

    def maxDown(self,position,endIndex):
        if self.heapSortableObj.hasRightChild(position,endIndex) and self.heapSortableObj.hasLeftChild(position,endIndex):
            if self.heapSortableObj.cmpValue_moreThan(self.heapSortableObj.leftChlidIndex(position),self.heapSortableObj.rightChildIndex(position)):
                if self.heapSortableObj.cmpValue_lessThan(position,self.heapSortableObj.leftChlidIndex(position)):
                    self.heapSortableObj.exchangeValue(position,self.heapSortableObj.leftChlidIndex(position))
                    self.maxDown(self.heapSortableObj.leftChlidIndex(position),endIndex)
            else:
                if self.heapSortableObj.cmpValue_lessThan(position,self.heapSortableObj.rightChildIndex(position)):
                    self.heapSortableObj.exchangeValue(position,self.heapSortableObj.rightChildIndex(position))
                    self.maxDown(self.heapSortableObj.rightChildIndex(position),endIndex)
        elif self.heapSortableObj.hasLeftChild(position,endIndex):
            if self.heapSortableObj.cmpValue_lessThan(position,self.heapSortableObj.leftChlidIndex(position)):
                self.heapSortableObj.exchangeValue(position,self.heapSortableObj.leftChlidIndex(position))
                self.maxDown(self.heapSortableObj.leftChlidIndex(position),endIndex)

    def buildHeap(self):
        endIndex = self.heapSortableObj.size - 1
        for i in range(self.heapSortableObj.getLastParentNodeIndex(endIndex) + 1)[::-1]:
            self.maxDown(i,endIndex)
        # for line in self.heapSortableObj.dataList:
        #     print line


    def maxSort(self):
        self.buildHeap()
        endIndex = self.heapSortableObj.size - 1
        self.heapSortableObj.exchangeValue(0,endIndex)
        while(endIndex > 0):
            endIndex -= 1
            self.maxDown(0,endIndex)
            self.heapSortableObj.exchangeValue(0,endIndex)
        if checkSort_Asc(self.heapSortableObj):
            print 'sort done : ' + self.heapSortableObj.name
        else:
            print 'sort failed'

    def write(self):
        self.heapSortableObj.write()

def HeapSortFilesUnderFolder(folderPath):
    fileNames = tm_com.getFileNamesFromFolder(folderPath)
    for fileName in fileNames:
        filePath = folderPath + fileName
        fileToSort = tm_SingleFile(filePath)
        heapSorter = tm_HeapSorter(fileToSort)
        heapSorter.maxSort()
        heapSorter.write()

def checkSort_Asc_Folder(folderPath):
    fileNames = tm_com.getFileNamesFromFolder(folderPath)
    for fileName in fileNames:
        filePath = folderPath + fileName
        fileToSort = tm_SingleFile(filePath)
        print checkSort_Asc(fileToSort)

def checkSort_Asc(heapSortableObj):
    if isinstance(heapSortableObj,tm_HeapSortable):
        for i in range(heapSortableObj.size - 1):
            if heapSortableObj.cmpValue_moreThan(i+1,i):
                pass
            else:
                # print str(i) + ' : ' + str(heapSortableObj.dataList[i])
                # print str(i + 1) + ' : ' + str(heapSortableObj.dataList[i+1])
                return False
        return True
    else:
        print('the value you pass id not a subclass of tm_HeaoSortable.')



# filePath = '/Users/Teemo/datasFile/divideFiles/sourceData_list/sourceData_part_1'
# lines = tm_com.getLinesFromFile(filePath)
# simpleDataList = tm_SimpleDataList(lines)
# heap = tm_HeapSorter(simpleDataList)
# start = time.time()
# heap.maxSort()
# end = time.time()
# print(str(end - start))
# print(checkSort_Asc(simpleDataList))

tempFilePath = '/Users/Teemo/datasFile/temp/'
fileNames = tm_com.getFileNamesFromFolder(tempFilePath)
print fileNames[0]
print fileNames[1]
h = []
h1 = tm_DividedFile(tempFilePath + fileNames[0])
h2 = tm_DividedFile(tempFilePath + fileNames[1])
h.append(h1)
h.append(h2)
hb = tm_FileDataList(h)
hb.exchangeValue(0,1)
print checkSort_Asc(hb)
# HeapSortFilesUnderFolder(tempFilePath)



