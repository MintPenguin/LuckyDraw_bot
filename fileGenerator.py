# winning_number.txt : 당첨번호
# nick_name.txt : 닉네임
# drawn_number.txt : 뽑은번호

import os.path

def dirExist(name):
    if not os.path.isdir(name):
        os.makedirs(name)

def fileExist(name):
    if not os.path.isfile(name):
        file = open(name, 'w')
        file.close()
        return False
    return True

def fileReader(name):

    returnArray = []

    with open(name, 'r') as file:
        lines = file.readlines()
        line = ''
        for line in lines:
            returnArray.append(line)
        return returnArray

def fileWriter(name, content):
    with open(name, 'a') as file:
        file.writelines(content + '\n')

def fileClear(name):
    with open(name, 'w') as file:
        None
