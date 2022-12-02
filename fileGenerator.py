# winning_number.txt : 당첨번호
# nick_name.txt : 닉네임
# drawn_number.txt : 뽑은번호

import os.path
from connectDB import *


class FileProc(Database):

    def __init__(self):
        pass

    def dirExist(self, name):
        if not os.path.isdir(name):
            os.makedirs(name)
            print('make a directory: {0}'.format(name))

    def fileExist(self, name):
        if not os.path.isfile(name):
            with open(name, 'w') as file:
                print('clear a file: {0}'.format(name))

        content = self.DBselect(name)
        if content is None:
            return

        with open(name, 'w') as file:
            file.writelines(content)
            print('overwrite a file({0}):'.format(name), content)

    def fileReader(self, name):
        returnArray = []

        try:
            with open(name, 'r') as file:
                lines = file.readlines()
                line = ''
                for line in lines:
                    returnArray.append(line)
            print('read a file({0}):'.format(name), returnArray)
        except Exception as e:
            print(e)

        return returnArray

    def fileWriter(self, name, content):

        content = content.strip()
        content += '\n'

        try:
            with open(name, 'a') as file:
                file.writelines(content)
                print('update a file({0}): (+)'.format(name), content)
        except Exception as e:
            print(e)

        content = ''.join(self.fileReader(name))
        self.DBupdate(name, content)

    def fileClear(self, name):
        try:
            with open(name, 'w') as file:
                print('clear a file: {0}'.format(name))

            self.DBupdate(name, '')
        except Exception as e:
            print(e)