#!/usr/bin/env python
#--*-- coding:utf-8 --*--
__author__ = 'Teemo'

import os

class tm_SplitFiles():

    def __init__(self, dir, file_name, file_postfix = '',  line_count = 10000):
        if dir[-1] != '/':
            self.dir = dir + '/'
        else:
            self.dir = dir
        self.file_name = file_name
        self.file_postfix = file_postfix
        self.line_count = line_count
        self.file_path = self.dir + self.file_name + self.file_postfix

    def split_file(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path) as file : # 使用with读文件
                    temp_count = 0
                    temp_content = []
                    part_num = 1
                    for line in file:
                        if temp_count < self.line_count:
                            temp_count += 1
                        else :
                            self.write_file(part_num, temp_content)
                            part_num += 1
                            temp_count = 1
                            temp_content = []
                        temp_content.append(line)
                    else :
                        self.write_file(part_num, temp_content)

            except IOError as err:
                print('IOError :'+ err)
        else:
            print("%s is not a validate file" % self.file_name)

    def get_part_file_path(self, part_num):
        divided_files_dir = self.dir + self.file_name + '_list/'
        if not os.path.exists(divided_files_dir) :
            os.makedirs(divided_files_dir)
        part_file_path = divided_files_dir + self.file_name + '_part_' + str(part_num) + self.file_postfix
        return part_file_path

    def write_file(self, part_num, *line_content):
        print('start processing part ' + str(part_num))
        part_file_path = self.get_part_file_path(part_num)
        try :
            with open(part_file_path, "w") as part_file:
                part_file.writelines(line_content[0])
        except IOError as err:
            print(err)

# if __name__ == "__main__":
#     import time
#     dir = '/Users/Teemo/datasFile/divideFiles/'
#     file_name = 'sourceData'
#     startTime = time.time()
#     spliteFile = tm_SplitFiles(dir,file_name)
#     spliteFile.split_file()
#     endTime = time.time()
#     print(str(endTime - startTime))