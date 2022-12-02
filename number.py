# last_number.txt: 뽑기판마지막번호
# limit_times.txt: 최대뽑기횟수
# prize.txt: (당첨등수)|(상품내용)|(상품이미지링크)\n(당첨등수)|(상품내용)|(상품이미지링크)\n...
# winning_number.txt : (당첨번호)|(당첨등수)\n(당첨번호)|(당첨등수)\n...
# nick_name.txt : 뽑은유저의닉네임\n뽑은유저의닉네임\n...
# drawn_number.txt : 뽑힌번호\n뽑힌번호\n뽑힌번호\n...

from fileGenerator import *
import random


class Check(FileProc):

    def __init__(self):
        pass

    # 처음 실행할 때
    def numberRun(self):
        global limitTimes, lastNumber, winningNumber
        global nickNameFile, drawnNumberFile, limitTimesFile, lastNumberFile, winningNumberFile, prizeFile

        self.checkFile(prizeFile, limitTimesFile, lastNumberFile, winningNumberFile, nickNameFile, drawnNumberFile)

        x = self.fileReader(limitTimesFile)
        limitTimes = int(x[0])

        x = self.fileReader(lastNumberFile)
        lastNumber = int(x[0])

        x = self.fileReader(winningNumberFile)
        for y in x: # ['255|1\n', '256|2\n']
            y = y.split('|') # ['255', '1\n']
            y = list(map(int, y)) # [255, 1]
            winningNumber[y[0]] = y[1]

    # 파일과 디렉토리에 오류가 있는지 확인한다.
    # 오류가 있다면 파일을 재생성하여 초기화한다.
    def checkFile(self, *args):
        global prizeFile, limitTimesFile, lastNumberFile, winningNumberFile, nickNameFile, drawnNumberFile
        global winningNumber, lastNumber, limitTimes

        for arg in args:

            self.__checkDirectory__(arg)
            self.fileExist(arg)

            file_contents = self.fileReader(arg)
            # 형식이 있는 파일만 아래에 추가한다.
            # prizeFile의 형식 : [<rank>|<goods>|[<goods image URL>]\n]
            # rank에는 반드시 1 이상의 값이 들어가있어야 한다.
            if arg == prizeFile:
                for fc in file_contents:
                    # prizeFile 파일 한줄에 하나라도 오류가 있따면
                    x = fc.strip('|')[0]
                    if not (x.strip().isdecimal()):
                        self.fileClear(arg)
                        break
                continue

            # limitTimesFile의 형식 : <int>\n, 무조건 하나
            elif arg == limitTimesFile:
                # limitTimesFile 파일에 오류가 있다면
                if not len(file_contents) == 1:
                    self.fileClear(arg)
                    self.fileWriter(arg, str(limitTimes))
                    continue
                if not (file_contents[0].strip().isdecimal() or (file_contents[0][0] == '-' and file_contents[0][1:].strip().isdecimal())):
                    self.fileClear(arg)
                    self.fileWriter(arg, str(limitTimes))
                    continue

            # lastNumberFile의 형식: <decimal>\n, 무조건 하나
            elif arg == lastNumberFile:
                # lastNumberFile 파일에 오류가 있다면
                if not len(file_contents) == 1:
                    self.fileClear(arg)
                    self.fileWriter(arg, str(lastNumber))
                    continue
                if not file_contents[0].strip().isdecimal():
                    self.fileClear(arg)
                    self.fileWriter(arg, str(lastNumber))
                    continue

            # winningNumberFile의 형식: <number>|<rank> \n <number>|<rank> \n...
            elif arg == winningNumberFile:
                # winningNumberFile 파일에 한 줄이라도 오류가 있다면
                for fc in file_contents:
                    if fc == '\n' and len(file_contents) == 1:
                        break
                    if not len(fc.strip().split('|')) == 2:
                        self.fileClear(arg)
                        r = random.randint(1, lastNumber)
                        winningNumber[r] = 1
                        self.fileWriter(arg, str(r) + "|1")
                        break
                    if not (fc.strip().split('|')[0].isdecimal() and fc.strip().split('|')[1].isdecimal()):
                        self.fileClear(arg)
                        r = random.randint(1, lastNumber)
                        winningNumber[r] = 1
                        self.fileWriter(arg, str(r) + "|1")
                        break
                continue

            # drawnNumberFile의 형식: <number> \n <number> \n ...
            elif arg == drawnNumberFile:
                # drawnNumberFile 파일에 한 줄이라도 오류가 있다면
                for fc in file_contents:
                    if not (fc.strip().isdecimal()):
                        self.fileClear(arg)
                        break
                continue


    # file_name이 './a/b/c.txt'이라면, ['a', 'b']으로 바꾼다.
    def __checkDirectory__(self, file_name):
        file_name = file_name.split('/') # ['.', 'a', 'b', 'c.txt']
        del file_name[-1] # ['.', 'a', 'b']
        del file_name[0] # ['a', 'b']

        for i in range(len(file_name)):
            self.dirExist('/'.join(file_name[:i + 1])) # 'a', 'a/b'


# 뽑기 횟수 업데이트 및 확인
class Count(Check):

    def __init__(self):
        global nickNameFile
        self.checkFile(nickNameFile)

    # 유저들의 뽑기 횟수를 0회로 초기화한다.
    def resetCount(self):
        global nickNameFile

        self.fileClear(nickNameFile)

    # 뽑기 횟수 제한을 count만큼 설정한다.
    def setLimitCount(self, count):
        global limitTimes, limitTimesFile
        limitTimes = count
        self.fileClear(limitTimesFile)
        self.fileWriter(limitTimesFile, str(count))


# 뽑기판 업데이트 및 확인
class Board(Check):

    def __init__(self):
        global drawnNumberFile, nickNameFile, lastNumberFile, winningNumberFile
        self.checkFile(drawnNumberFile, nickNameFile, lastNumberFile, winningNumberFile)

    # 뽑기를 number만큼 생성한다.
    def setBoard(self, number):
        global winningNumber, lastNumber
        global drawnNumberFile, nickNameFile, lastNumberFile, winningNumberFile

        try:
            self.fileClear(drawnNumberFile)
            self.fileClear(lastNumberFile)
            self.fileClear(nickNameFile)

            lastNumber = number
            self.fileWriter(lastNumberFile, str(number))

            # 당첨 번호와 당첨번호의 당첨 등수가 1인 뽑기를 한개로 초기화한다.
            winningNumber.clear()
            self.fileClear(winningNumberFile)
            w = Winning()
            w.addWinningNumber(1, 1)
        except Exception as e:
            print('error:', e)

    # 뽑기의 남은 숫자를 확인한다.
    # 남은 숫자를 list()로 반환한다.
    def remainingNumber(self):
        global lastNumber, drawnNumberFile

        # 반환타입: list
        # 반환값: 남은 숫자
        returnArray = list()

        # 초기에 설정한 뽑기판의 뽑기 번호를 불러온다.
        for i in range(lastNumber):
            returnArray.append(i + 1)

        # 이미 뽑힌 뽑기 번호를 불러온다.
        drawn = self.fileReader(drawnNumberFile)

        # 초기에 설정한 뽑기판의 뽑기 번호에서 이미 뽑힌 번호는 하나씩 삭제한다.
        for d in drawn:
            for a in returnArray:
                if int(d) == a:
                    returnArray.remove(a)
                    break

        return returnArray


# 업데이트 당첨 개수 및 확인
class Winning(Check):

    def __init__(self):
        global winningNumberFile
        self.checkFile(winningNumberFile)

    # 당첨 번호를 amount만큼 rank등수에 추가한다.
    # 반환값: 추가 작업 후 해당 랭크의 당첨 번호 개수
    def addWinningNumber(self, amount, rank):
        global lastNumber, winningNumberFile, winningNumber

        try:
            ret = 0

            # 이미 뽑힌 번호에 당첨이 나오지 않게 하기 위해 남은 번호를 불러온다.
            remain = Board()
            remain = remain.remainingNumber()  # [2, 3, 6, 7, 10, 15] (남아 있는 전체 번호)

            # 남아있는 전체 번호에서 이미 등록되어 있는 당첨번호를 삭제한다.
            for i in winningNumber.keys():
                remain.remove(i)

            # 당첨번호를 amount 만큼 추가한다.
            for a in range(amount):
                # 당첨 번호를 더이상 추가할 수 없으면 추가하지 않는다.
                if len(remain) == 0:
                    break
                r = random.randint(0, len(remain) - 1)
                winningNumber[remain[r]] = rank
                del remain[r]

            # '당첨번호|등수<rank>'을 파일에 수정한다.
            self.fileClear(winningNumberFile)
            s = ''
            for k, v in winningNumber.items():
                s += str(k) + '|' + str(v) + '\n'
                if v == rank:
                    ret += 1
            self.fileWriter(winningNumberFile, s)

            return ret
        except Exception as e:
            print('error:', e)

    # rank등수에 해당하는 당첨 번호를 amount만큼 삭제한다.
    # 반환값: 삭제 작업 후 해당 랭크의 당첨 번호 개수
    def delWinningNumber(self, amount, rank):

        global winningNumber, winningNumberFile

        ret = 0
        w = list()  # rank등수에 해당하는 당첨 번호 [25, 342, 3]를 넣을 변수

        # rank 등수에 해당하는 당첨 번호를 불러온다.
        for k, v in winningNumber.items():
            if v == rank:
                w.append(k)

        # amount 만큼 당첨번호를 삭제한다.
        for i in range(amount):
            if len(w) == 0:
                break
            r = random.randint(0, len(w) - 1)
            del winningNumber[w[r]]
            del w[r]

        # 당첨 번호 파일(winning_number.txt)을 수정한다.
        self.fileClear(winningNumberFile)
        s = ''
        for k, v in winningNumber.items():
            s += str(k) + '|' + str(v) + '\n'
            if v == rank:
                ret += 1
        self.fileWriter(winningNumberFile, s)

        return ret

    # 당첨이 몇개있는지
    # 반환: {랭크: 해당하는 당첨 개수}
    def viewWinningNumber(self):
        global winningNumber

        ret = dict()

        b = Board()
        b = b.remainingNumber()

        for k, v in winningNumber.items(): # k: 번호, v: 랭크
            if k in b: # 보드판에 번호가 있다면
                if v in ret: # 랭크가 처음 등록되는 거면 1로 등록, 아니라면 1을 더함.
                    ret[v] += 1
                else:
                    ret[v] = 1

        return ret

# 뽑기판 뽑기에 관하여
class Draw(Check):

    def __init__(self):
        global drawnNumberFile, nickNameFile, winningNumberFile
        self.checkFile(drawnNumberFile, nickNameFile, winningNumberFile)

    # 뽑기가 당첨 번호인지 확인한다.
    # return: (<winning code>, <winning rank>)
    # 당첨이 아닐 경우 당첨 랭크를 0으로 반환
    def isWinning(self, number, discordID):
        global limitTimes, drawnNumberFile, nickNameFile, winningNumberFile

        # 뽑기 번호의 최댓값과 최솟값을 벗어났다면
        if 1 > number or lastNumber < number:
            return (-1, 0)

        # 이미 뽑힌 번호라면
        drawnNumbers = self.fileReader(drawnNumberFile)
        for dn in drawnNumbers:
            if int(dn) == number:
                return (2, 0)

        # 뽑기 횟수 제한이 걸려있다면
        nickNameList = self.fileReader(nickNameFile)
        times = 0
        for nl in nickNameList:
            if int(nl) == discordID:
                times += 1
        if limitTimes <= times and limitTimes >= 0:  # 뽑기 횟수 제한이 0 이상이고 뽑은 횟수보다 많을 때
            return (3, 0)

        # 위에 해당하지 않는다면 해당 번호를 뽑는다.
        self.fileWriter(nickNameFile, str(discordID))
        self.fileWriter(drawnNumberFile, str(number))
        for k, v in winningNumber.items():
            # 당첨 번호를 뽑았다면 당첨번호(winning_number.txt)에 해당하는 번호를 삭제한다.
            if k == number:
                del winningNumber[k]
                self.fileClear(winningNumberFile)
                s = ''
                for k, v in winningNumber.items():
                     s += str(k) + '|' + str(v) + '\n'
                self.fileWriter(winningNumberFile, s)
                return (1, v)

        # 꽝 번호를 뽑았다면
        return (0, 0)


class Prize(Check):

    def __init__(self):
        global prizeFile
        self.checkFile(prizeFile)

    # rank순위에 맞는 상품(prize)을 추가한다.
    def addPrize(self, rank, prize, imageURL):
        global prizeFile

        # 같은 rank가 있는지 prize 파일에서 확인한다.
        prizeList = self.fileReader(prizeFile)

        for i in range(len(prizeList)):
            if int(prizeList[i].split('|')[0]) == rank:
                prizeList[i] = '{0}|{1}|{2}'.format(str(rank), prize, imageURL)
                self.fileClear(prizeFile)
                self.fileWriter(prizeFile, '\n'.join(prizeList))
                return

        # 만약 같은 rank가 없다면 새로 생성한다.
        self.fileWriter(prizeFile, '{0}|{1}|{2}'.format(str(rank), prize, imageURL))

    # rank 순위에 맞는 상품(prize)을 삭제한다.
    def delPrize(self, rank):
        global prizeFile

        prizeList = self.fileReader(prizeFile)

        for i in range(len(prizeList)):
            if int(prizeList[i].split('|')[0]) == rank:
                del prizeList[i]
                self.fileClear(prizeFile)
                self.fileWriter(prizeFile, '\n'.join(prizeList))
                return

    # 모든 상품을 삭제한다.
    def clearPrize(self):
        global prizeFile
        self.fileClear(prizeFile)

    # 모든 상품을 확인한다.
    def viewPrize(self):
        global prizeFile
        prizeList = self.fileReader(prizeFile)

        return prizeList

# ====== 변수 ======
dataDirectory = './data'
prizeFile = dataDirectory + '/prize.txt'
limitTimesFile = dataDirectory + '/limit_times.txt'
lastNumberFile = dataDirectory + '/last_number.txt'
winningNumberFile = dataDirectory + '/winning_number.txt'
nickNameFile = dataDirectory + '/nick_name.txt'
drawnNumberFile = dataDirectory + '/drawn_number.txt'

winningNumber = dict()
lastNumber = 100
limitTimes = 3
