__author__ = 'Teemo'
import os
import tm_com
import time
import someOldCodes

debug = False


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

    def item(self,positon):
        return self.dataList[positon]

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
    def exchangeValue(self,node,child):
        pass

    @abstractmethod
    def putMaxValueToNode(self,node,child):
        pass

class tm_SingleFile(tm_HeapSortable):

    def __init__(self,filePath):
        self.filePath = filePath
        lines = tm_com.getLinesFromFile(filePath)
        self.name = filePath
        # super(tm_HeapSortable,self).__init__(lines)
        self.dataList = lines
        self.size = len(lines)

    def exchangeValue(self,node,child):
        temp = self.dataList[child]
        self.dataList[child] = self.dataList[node]
        self.dataList[node] = temp

    def putMaxValueToNode(self,node,child):
        if self.dataList[node] < self.dataList[child]:
            self.exchangeValue(node,child)

    def write(self):
        tm_com.writeLines(self.filePath,self.dataList)
        print 'write done : ' + self.name

class tm_DividedFile():
    def __init__(self,fileFolder,fileName):
        self.fileFolder = fileFolder
        self.fileName = fileName
        self.filePath = fileFolder + fileName
        self.lines = tm_com.getLinesFromFile(self.filePath)
        self.size = len(self.lines)
        self.start = self.lines[0]
        self.end = self.lines[-1]

    def __lt__(self, other):
        if self.end < other.start:
            return True
        else:
            return False

    def __le__(self, other):
        if self.end <= other.start:
            return True
        else:
            return False

    def __gt__(self, other):
        if self.start > other.end:
            return True
        else:
            return False

    def __ge__(self, other):
        if self.start >= other.end:
            return True
        else:
            return False

    def __eq__(self, other):
        if self.start == other.start and self.end == other.end:
            return True
        else:
            return False

    def __str__(self):
        description = self.fileName + tm_com.line_feed
        description += self.start + tm_com.line_feed
        description += self.end + tm_com.line_feed
        return description

    __repr__ = __str__

class tm_FileDataList(tm_HeapSortable):
    def __init__(self,folderPath):
        fileNames = tm_com.getFileNamesFromFolder(folderPath)
        self.dataList = []
        for fileName in fileNames:
            self.dataList.append(tm_DividedFile(folderPath,fileName))
        self.size = len(self.dataList)
        self.name = folderPath

    def putMaxValueToNode(self,node,child):
        if debug:
            print '**************************'
            print 'exchange : ' + tm_com.line_feed
            print self.dataList[node]
            print self.dataList[child]
        nodeIndexFileSize = self.dataList[node].size
        childIndexFileSize = self.dataList[child].size
        biggerSize = max(nodeIndexFileSize,childIndexFileSize)
        allLines = []
        i = 0
        j = 0
        while i < self.dataList[node].size and j < self.dataList[child].size:
            if self.dataList[node].lines[i] < self.dataList[child].lines[j]:
                allLines.append(self.dataList[node].lines[i])
                i += 1
            else:
                allLines.append(self.dataList[child].lines[j])
                j += 1
        if i < nodeIndexFileSize:
            allLines.extend(self.dataList[node].lines[i:])
        else:
            allLines.extend(self.dataList[child].lines[j:])

        litterArray = allLines[:biggerSize]
        biggerArray = allLines[biggerSize:]
        os.remove(self.dataList[node].filePath)
        tm_com.writeLines(self.dataList[node].filePath,biggerArray)
        os.remove(self.dataList[child].filePath)
        tm_com.writeLines(self.dataList[child].filePath,litterArray)
        self.dataList[node] = tm_DividedFile(self.dataList[node].fileFolder,self.dataList[node].fileName)
        self.dataList[child] = tm_DividedFile(self.dataList[child].fileFolder,self.dataList[child].fileName)
        if debug:
            print 'after exchange: ' + tm_com.line_feed
            print self.dataList[node]
            print self.dataList[child]
            print '**************************'

    def exchangeValue(self,node,child):
        os.remove(self.dataList[node].filePath)
        tm_com.writeLines(self.dataList[node].filePath,self.dataList[child].lines)
        os.remove(self.dataList[child].filePath)
        tm_com.writeLines(self.dataList[child].filePath,self.dataList[node].lines)
        self.dataList[node] = tm_DividedFile(self.dataList[node].fileFolder,self.dataList[node].fileName)
        self.dataList[child] = tm_DividedFile(self.dataList[child].fileFolder,self.dataList[child].fileName)

    def write(self):
        for i in range(self.size):
            os.rename(self.dataList[i].filePath, self.dataList[i].fileFolder + "sorted_" +str(i) )

class tm_HeapSorter():

    def __init__(self,heapSortableObj):
        if isinstance(heapSortableObj,tm_HeapSortable):
            self.heapSortableObj = heapSortableObj
        else:
            print('the value you pass id not a subclass of tm_HeaoSortable.')

    def item(self,positon):
        return self.heapSortableObj.item(positon)

    def hasRightChild(self,position,endIndex):
        return self.heapSortableObj.hasRightChild(position,endIndex)

    def hasLeftChild(self,position,endIndex):
        return self.heapSortableObj.hasLeftChild(position,endIndex)

    def rightChild(self,position):
        return self.heapSortableObj.rightChild(position)

    def leftChild(self,position):
        return self.heapSortableObj.leftChild(position)

    def exchangeValue(self,node,child):
        self.heapSortableObj.exchangeValue(node,child)

    def rightChildIndex(self,index):
        return self.heapSortableObj.rightChildIndex(index)

    def leftChlidIndex(self,index):
        return self.heapSortableObj.leftChlidIndex(index)

    def putMaxValueToNode(self,node,child):
        self.heapSortableObj.putMaxValueToNode(node,child)

    def maxDown(self,position,endIndex):
        if self.hasRightChild(position,endIndex) and self.hasLeftChild(position,endIndex):
            if self.leftChild(position) >= self.rightChild(position):
                if not self.item(position) >= self.leftChild(position):
                    self.putMaxValueToNode(position,self.leftChlidIndex(position))
                    self.maxDown(self.leftChlidIndex(position),endIndex)

            elif self.rightChild(position) >= self.leftChild(position):
                if not self.item(position) >= self.rightChild(position):
                    self.putMaxValueToNode(position,self.rightChildIndex(position))
                    self.maxDown(self.rightChildIndex(position),endIndex)

            elif not self.leftChlidIndex(position) == self.rightChildIndex(position):
                self.putMaxValueToNode(self.leftChlidIndex(position),self.rightChildIndex(position))
                self.putMaxValueToNode(position,self.leftChlidIndex(position))
                self.maxDown(self.leftChlidIndex(position),endIndex)
                self.maxDown(self.rightChildIndex(position),endIndex)

        elif self.hasLeftChild(position,endIndex):
            if not self.item(position) >= self.leftChild(position):
                self.putMaxValueToNode(position,self.leftChlidIndex(position))
                self.maxDown(self.leftChlidIndex(position),endIndex)

    def buildHeap(self):
        endIndex = self.heapSortableObj.size - 1
        for i in range(self.heapSortableObj.getLastParentNodeIndex(endIndex) + 1)[::-1]:
            # self.maxDown(i,endIndex)
            self.maxDown(i,endIndex)

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
    print fileNames
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
        print filePath
        print checkSort_Asc(fileToSort)

def checkSort_Asc(heapSortableObj):
    if isinstance(heapSortableObj,tm_HeapSortable):
        for i in range(heapSortableObj.size - 1):
            if heapSortableObj.dataList[i+1] >= heapSortableObj.dataList[i]:
                pass
            else:
                print heapSortableObj.dataList[i+1]
                print heapSortableObj.dataList[i]
                return False
        return True
    else:
        print('the value you pass id not a subclass of tm_HeaoSortable.')

def checkSort_Des(heapSortableObj):
    if isinstance(heapSortableObj,tm_HeapSortable):
        for i in range(heapSortableObj.size - 1):
            if heapSortableObj.dataList[i+1] <= heapSortableObj.dataList[i]:
                pass
            else:
                print heapSortableObj.dataList[i+1]
                print heapSortableObj.dataList[i]
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
start = time.time()



tempFilePath = '/Users/Teemo/datasFile/temp/'

HeapSortFilesUnderFolder(tempFilePath)
fileListToSort = tm_FileDataList(tempFilePath)
sorter = tm_HeapSorter(fileListToSort)
sorter.maxSort()
sorter.write()

# checkSort_Asc_Folder(tempFilePath)


end = time.time()
print(str(end - start))


