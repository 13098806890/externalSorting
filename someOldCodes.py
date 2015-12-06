__author__ = 'Teemo'
import tm_com

#class start
class tm_TreeNode:

    def __init__(self,value = None):
        self.value = value
        self.leftChild = None
        self.rigthChild = None

    @property
    def value(self):
        return self.value

    @value.setter
    def value(self,value):
        self.value = value

    @property
    def leftChild(self):
        return self.leftChild

    @leftChild.setter
    def leftChild(self,leftChild):
        if isinstance(leftChild,tm_TreeNode):
            self.leftChild = leftChild

    @property
    def rightChild(self):
        return self.leftChild

    @rightChild.setter
    def rightChild(self,rightChild):
        if isinstance(rightChild,tm_TreeNode):
            self.rightChild = rightChild

    def __str__(self):
        description = str(self.value) + tm_com.line_feed
        description += 'left : ' + str(self.leftChild) + tm_com.line_feed
        description += 'right : ' + str(self.rightChild) + tm_com.line_feed
        return description

    __repr__ = __str__

#class end

#class
class tm_Tree:

    def __init__(self):
        self.root =tm_TreeNode()
        self.size = 0

    def insertLeft(self,treeNode,data):
        if isinstance(treeNode,tm_TreeNode):
            newTreeNode = tm_TreeNode(data)
            treeNode.leftChild = newTreeNode
        else:
            print('invalid treeNode.')

    def insertRight(self,treeNode,data):
        if isinstance(treeNode,tm_TreeNode):
            newTreeNode = tm_TreeNode(data)
            treeNode.rightChild = newTreeNode
        else:
            print('invalid treeNode.')
# class end

class tm_Heap():

    def __init__(self,values):
        if isinstance(values,list):
            self.dataList = values
            self.size = len(values)
        else:
            print("values : " + str(values))
            print ("init failed, the 'values' you passed is not a list.")

    def exchangeValue(self,fromIndex,toIndex):
        temp = self.dataList[fromIndex]
        self.dataList[fromIndex] = self.dataList[toIndex]
        self.dataList[toIndex] = temp

    def leftChlidIndex(self,index):
        return 2 * index + 1

    def rightChildIndex(self,index):
        return 2 * index + 2

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
        return (endIndex-1)/2

    def maxDown(self,position,endIndex):
        if self.hasRightChild(position,endIndex) and self.hasLeftChild(position,endIndex):
            if self.dataList[self.leftChlidIndex(position)] > self.dataList[self.rightChildIndex(position)]:
                if self.dataList[position] < self.dataList[self.leftChlidIndex(position)]:
                    self.exchangeValue(position,self.leftChlidIndex(position))
                    self.maxDown(self.leftChlidIndex(position),endIndex)
            else:
                if self.dataList[position] < self.dataList[self.rightChildIndex(position)]:
                    self.exchangeValue(position,self.rightChildIndex(position))
                    self.maxDown(self.rightChildIndex(position),endIndex)
        elif self.hasLeftChild(position,endIndex):
            if self.dataList[position] < self.dataList[self.leftChlidIndex(position)]:
                self.exchangeValue(position,self.leftChlidIndex(position))
                self.maxDown(self.leftChlidIndex(position),endIndex)

    def buildHeap(self):
        endIndex = self.size
        for i in range(self.getLastParentNodeIndex(endIndex))[::-1]:
            self.maxDown(i,endIndex)

    def maxSort(self):
        self.buildHeap()
        endIndex = self.size - 1
        self.exchangeValue(0,endIndex)
        while(endIndex > 0):
            endIndex -= 1
            self.maxDown(0,endIndex)
            self.exchangeValue(0,endIndex)



    def __str__(self):
        description = ''
        for item in self.dataList:
            description += item + tm_com.line_feed
        return description

    __repr__ = __str__

#class end

def checkSort(lines):
    for i in range(len(lines) - 1):
        if lines[i+1] > lines[i]:
            pass
        else:
            print str(i) + ' : ' + str(lines[i])
            print str(i + 1) + ' : ' + str(lines[i+1])
            return False
    return True