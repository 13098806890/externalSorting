__author__ = 'Teemo'
#!/usr/bin/env python
#--*-- coding:utf-8 --*--

# suppose the files need to sorted in below dir :
# I need a fileIndex to manager the list files to do my outer sorting
#divideFiles:
#           sourceData(the source need to sort, very huge and can not loaded to memory once)
#           sourceData_list:(hold the list files of the source data, They are divided by lines)
#                           part1(part one of the source data)
#                           part2
#                           part3
#                           .....
#                           partn
#
#           fileIndex(a file to manager the list files)
#           tempFolder:(just some tempfiles in this forlder for sorting)


# in the index file , I will use below format to record
#  <fileindex>
#        <group>
#               <groupstart>aTd7o6R71ATZ/14yZHYr</groupstart>
#               <groupend>ti3uQI1lrzrLDMCIz5yh</groupend>
#        		<file>
#        			<filename>sourceData_part_1</filename>
#        			<start>aTd7o6R71ATZ/14yZHYr</start>
#        			<end>ti3uQI1lrzrLDMCIz5yh</end>
#        		</file>
#
#        		<file>
#        			...........
#        		</file>
#         </group>
#
#         <group>
#         	.......
#         </group>
#
#  </fileindex>


import os
import tm_com
import time
from xml.etree import ElementTree

#class start
class tm_Sorted_file_manager():
    def __init__(self,dir,list_folder,temp_folder):
        self.dir = dir
        self.list_folder = list_folder
        self.temp_folder = temp_folder
        self.file_list = self.getListfiles()

    def getListfiles(self):

        def cmpFileByPartNumber(file_name_1,file_name_2):
            # the file name is xxx_part_number
            number_1 = int(file_name_1.split('part_')[1])
            number_2 = int(file_name_2.split('part_')[1])
            if number_1 > number_2:
                return 1
            else:
                return -1

        if os.path.exists(self.list_folder):
            files = os.listdir(self.list_folder)
            for file in files:
                if file[0] == '.':
                    files.remove(file)
            return sorted(files,cmpFileByPartNumber)
        else:
            return None
#class end

#class tm_part_file()
class tm_Part_file():
    def __init__(self,file_name,start,end):
        self.file_name = file_name
        self.start = start
        self.end = end
    def xml(self):
        xmlString = '<file>' + tm_com.line_feed
        xmlString += '  <filename>' + self.file_name + '</filename>' + tm_com.line_feed
        xmlString += '  <start>' + self.start + '</start>' + tm_com.line_feed
        xmlString += '  <end>' + self.end + '</end>' +tm_com.line_feed
        xmlString +='</file>'
        return xmlString

    def __str__(self):
        description = ''
        description += '  filename : ' + self.file_name + tm_com.line_feed
        description += 'startindex : ' + self.start + tm_com.line_feed
        description += '  endindex : ' + self.end + tm_com.line_feed
        return description

    __repr__ = __str__
#class end


#class tm_sorted_group()
class tm_Sorted_group():
    def __init__(self):
        self.files = []
        self.files_number = 0

    def addFile(self,file):
        if isinstance(file,tm_Part_file):
            self.files.append(file)
            self.files_number += 1

    def removeFile(self,file):
        if isinstance(file,tm_Part_file):
            self.files.remove(file)
            self.files_number -= 1

    def startIndex(self):
        if len(self.files) > 0:
            return self.files[0].start

    def endIndex(self):
        if len(self.files) > 0:
            return self.files[-1].end

    def xml(self):
        xmlString = '<group>' + tm_com.line_feed
        xmlString += '  <groupstart>' + self.startIndex() + '</groupstart>' +tm_com.line_feed
        xmlString += '  <groupend>' + self.endIndex() + '</groupend>' +tm_com.line_feed
        xmlString += ''
        for file in self.files:
            for line in file.xml().split(tm_com.line_feed):
                xmlString += '  ' + line + tm_com.line_feed
        xmlString += '</group>' + tm_com.line_feed
        return xmlString

    def __str__(self):
        description = ''
        description += '     group : ' + tm_com.line_feed
        description += 'groupstart : ' + self.startIndex() + tm_com.line_feed
        description += tm_com.line_feed
        for file in self.files:
            for line in str(file).split(tm_com.line_feed):
                description += '    ' + line + tm_com.line_feed
        description += '  groupend : ' + self.endIndex() + tm_com.line_feed
        return description

    __repr__ = __str__
#class end


#class start
class tm_Sorted_file_index():
    def __init__(self):
        pass
#class end


#class start
class tm_Index_Groups():
    def __init__(self,root_tag,group_tag, groupstart_tag,
                 groupend_tag,file_tag, filename_tag, start_tag, end_tag):
        self.group_files_folder = ''
        self.groups = []
        self.root_tag = root_tag
        self.group_tag = group_tag
        self.groupstart_tag = groupstart_tag
        self.groupend_tag = groupend_tag
        self.file_tag = file_tag
        self.filename_tag = filename_tag
        self.start_tag = start_tag
        self.end_tag = end_tag

    def setGroupFilesFolder(self,group_files_folder):
        self.group_files_folder = group_files_folder

    def addGroup(self,group):
        if isinstance(group,tm_Sorted_group):
            self.groups.append(group)

    def getGroupsCount(self):
        return str(len(self.groups))

    def xml(self):
        xmlString = '<?xml version="1.0" ?>' + tm_com.line_feed
        xmlString += '<fileindex>' + self.group_files_folder + tm_com.line_feed
        for group in self.groups:
            for line in group.xml().split(tm_com.line_feed):
                xmlString += '  ' + line + tm_com.line_feed
        xmlString += '</fileindex>' + tm_com.line_feed
        return xmlString

    def writeXml(self,filePath):
        os.remove(filePath)
        outPutFile = open(filePath,'a')
        for line in self.xml().split(tm_com.line_feed):
            outPutFile.write(line)
            outPutFile.write(tm_com.line_feed)
        outPutFile.close()

    def __str__(self):
        description = self.root_tag + ' : ' + tm_com.line_feed
        description += "group files folder : " + self.group_files_folder
        for group in self.groups:
            for line in str(group).split(tm_com.line_feed):
                description += '    ' + line + tm_com.line_feed
        return description

    __repr__ = __str__

#class end

#class start
class tm_Index_xml_parser():

    def __init__(self, index_file_path, root_tag = 'fileindex', group_tag = 'group', groupstart_tag = 'groupstart',
                 groupend_tag = 'groupend', file_tag = 'file', filename_tag = 'filename', start_tag = 'start', end_tag = 'end' ):
        self.index_file_path = index_file_path
        self.index_file_dir = os.path.dirname(self.index_file_path) + '/'
        self.index_file_name = str(index_file_path).replace(self.index_file_dir,'')
        self.temp_index_file_name = 'temp_' + self.index_file_name
        self.temp_index_file_path = self.index_file_dir + self.temp_index_file_name
        self.index_groups = tm_Index_Groups(root_tag, group_tag, groupstart_tag, groupend_tag, file_tag, filename_tag, start_tag, end_tag)

    def generateXML(self,tm_index_groups):
        if isinstance(tm_index_groups,tm_Index_Groups):
            pass
        else:
            print('can not generate xml file cause the input is not a tm_Index_Groups')


    def parseXML(self):
        dom = ElementTree.parse(self.index_file_path)
        rootNode = dom.getroot()
        if rootNode.tag == self.index_groups.root_tag:
            self.index_groups.setGroupFilesFolder(rootNode.text)
            for groupNode in rootNode.getchildren():
                if groupNode.tag == self.index_groups.group_tag:
                    self.index_groups.addGroup(self.getGroup(groupNode))
            return True
        else :
            print (rootNode.tag + ' : ' + self.index_groups.root_tag)
            print ('the xml file you parse is not the correct format.')
            return False

    def getGroup(self,groupNode):
        group = tm_Sorted_group()
        for fileNode in groupNode.getchildren():
            if fileNode.tag == self.index_groups.file_tag:
                group.addFile(self.getFile(fileNode))
        return group

    def getFile(self,fileNode):
        filename = ''
        start = ''
        end = ''
        for item in fileNode.getchildren():
            tag = item.tag
            if tag == self.index_groups.filename_tag:
                filename = item.text
            elif tag == self.index_groups.start_tag:
                start = item.text
            elif tag == self.index_groups.end_tag:
                end = item.text
            else:
                print('wrong xml tag in the file node')
        file = tm_Part_file(filename,start,end)
        return file

#class end


# dir = '/Users/Teemo/datasFile/divideFiles/'
# list_folder = dir + 'sourceData_list'
# temp_folder = dir + 'tempFolder'
#
# tm_manager = tm_SortedFileManagement(dir,list_folder,temp_folder)
start = time.time()
index_file_path = '/Users/Teemo/datasFile/file_index_example.xml'
temp_file_path = '/Users/Teemo/datasFile/file_index_example_temp.xml'
index_phraser = tm_Index_xml_parser(index_file_path)
index_phraser.parseXML()
index_phraser.index_groups.writeXml(temp_file_path)
index_phraser1 = tm_Index_xml_parser(temp_file_path)
index_phraser1.parseXML()
end = time.time()
print(str(index_phraser1.index_groups.xml()))
# print(tm_Sorted_file_management.getListfiles())