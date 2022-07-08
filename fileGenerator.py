# winning_number.txt : 당첨번호
# nick_name.txt : 닉네임
# drawn_number.txt : 뽑은번호

import os.path
from connectDB import *

def createDatabaseTable():
    DBcreateTable()

def dirExist(name):
    if not os.path.isdir(name):
        os.makedirs(name)
        print('make a directory: {0}'.format(name))

def fileExist(name):
    if not os.path.isfile(name):
        with open(name, 'w') as file:
            print('clear a file: {0}'.format(name))

    content = DBselect(name)
    if content is None:
        return

    with open(name, 'w') as file:
        file.writelines(content)
        print('overwrite a file({0}):'.format(name), content)

def fileReader(name):

    returnArray = []

    with open(name, 'r') as file:
        lines = file.readlines()
        line = ''
        for line in lines:
            returnArray.append(line)

    print('read a file({0}):'.format(name), returnArray)

    return returnArray

def fileWriter(name, content):
    content += '\n'
    with open(name, 'a') as file:
        file.writelines(content)
        print('update a file({0}): (+)'.format(name), content)

    content = ''.join(fileReader(name))
    DBupdate(name, content)

def fileClear(name):
    with open(name, 'w') as file:
        print('clear a file: {0}'.format(name))

    DBupdate(name, '')
