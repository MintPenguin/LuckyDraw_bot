# winning_number.txt : 당첨번호
# nick_name.txt : 닉네임
# drawn_number.txt : 뽑은번호

from fileGenerator import *
import random

def winningNumberGenerator(numbers):
    for number in numbers:
        fileWriter(winningNumberFile, str(number))

def numberRun():

    global dataDirectory, lastNumberFile, winningNumber, lastNumber, winningNumberFile, nickNameFile, drawnNumberFile, limitTimes, limitTimesFile

    dirExist(dataDirectory)

    fileExist(nickNameFile)
    fileExist(drawnNumberFile)

    if fileExist(limitTimesFile):
        limitTimes = int(fileReader(limitTimesFile)[0])
    else:
        limitTimes = 3
        fileWriter(limitTimesFile, str(limitTimes))

    if fileExist(lastNumberFile):
        lastNumber = int(fileReader(lastNumberFile)[0])
    else:
        lastNumber = 1
        fileWriter(lastNumberFile, str(lastNumber))

    if fileExist(winningNumberFile):
        winningNumber = fileReader(winningNumberFile)
        winningNumber = list(map(int, winningNumber))
    else:
        setWinningNumber()

def setLastNumber(command):
    global lastNumber, drawnNumberFile, nickNameFile, lastNumberFile
    fileClear(drawnNumberFile)
    fileClear(nickNameFile)
    fileClear(lastNumberFile)
    lastNumber = int(command)
    fileWriter(lastNumberFile, command)
    setWinningNumber()

def setWinningNumber():
    global lastNumber, winningNumberFile, winningNumber
    winningNumber.clear()
    fileClear(winningNumberFile)
    winningNumber.append(random.randint(1, lastNumber))
    winningNumberGenerator(winningNumber)

def setlimitTimes(count):
    global limitTimes, limitTimesFile
    limitTimes = int(count)
    fileClear(limitTimesFile)
    fileWriter(limitTimesFile, count)


def isWinning(number, discordID):
    global limitTimes

    if 1 > int(number) or lastNumber < int(number):
        return -1

    drawnNumbers = fileReader(drawnNumberFile)
    for dn in drawnNumbers:
        if int(dn) == int(number):
            return 2

    nickNameList = fileReader(nickNameFile)
    times = 0
    for nl in nickNameList:
        if int(nl) == discordID:
            times += 1
    if limitTimes <= times and limitTimes >= 0:
        return 3

    fileWriter(nickNameFile, str(discordID))
    fileWriter(drawnNumberFile, number)

    for n in winningNumber:
        if n == int(number):
            return 1

    return 0

def remainingNumber():

    global lastNumber, drawnNumberFile

    returnArray = []

    for i in range(lastNumber):
        returnArray.append(i + 1)

    drawn = fileReader(drawnNumberFile)

    for d in drawn:
        for a in returnArray:
            if int(d) == a:
                returnArray.remove(a)
                break

    return returnArray

# ====== 변수 ======
dataDirectory = './data'
limitTimesFile = dataDirectory + '/limit_times.txt'
lastNumberFile = dataDirectory + '/last_number.txt'
winningNumberFile = dataDirectory + '/winning_number.txt'
nickNameFile = dataDirectory + '/nick_name.txt'
drawnNumberFile = dataDirectory + '/drawn_number.txt'

winningNumber = []
lastNumber = 1
limitTimes = 3
