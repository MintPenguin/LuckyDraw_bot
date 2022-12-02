#run.py
import discord
from discord.ext import commands
from number import *
import threading, requests
#import sys

##draw 2

##view board > ##board view
##reset board 1024 > ##board set 1024

##add winning 50 5 > ##winning add 50 5
##delete winning 35 4 > ##winning delete 35 4
##> ##winning remain

##set count -1 > ##count limit -1
##clear count > ##count reset

##set prize 2 100golds http > ##prize set 2 100golds http
##> ##prize delete 2
##> ##prize clear
##> ##prize list

TOKEN = os.environ.get('LUCKY_DRAW_TOKEN')
REPLE = os.environ.get('REPLE')
bot = discord.Client()
command_prefix = '##'
bot = commands.Bot(command_prefix=command_prefix)

@bot.event
async def on_ready():
    #print(sys.executable)
    startTimer()
    c = Check()
    c.numberRun()
    print('We have logged in as {0.user}\n=========='.format(bot))

@bot.event
async def on_command_error(ctx, error):
#    return
    if isinstance(error, commands.CommandNotFound):
#    	await ctx.send("command not found")
        print(error)
    print('==========')

@bot.command()
async def board(ctx, *command):
    print('{0}({1}): board {2}'.format(ctx.author, ctx.author.id, ' '.join(command)))

    message = ''
    embed = None

    if len(command) == 0:
        message = '`{0}board view` : View remaining numbers of board.\n'.format(command_prefix)
        message += '`{0}board set <the number of draws>` : Set the board with the number of draws.'.format(command_prefix)
    elif command[0] == 'view':
        text = ''
        b = Board()
        numberList = b.remainingNumber()

        for nl in numberList:
            text += str(nl) + ' '

        embed = discord.Embed(title="remaining numbers: {0}".format(str(len(numberList))), description=text,
                              color=0x808080)
    elif command[0] == 'set':
        if ctx.message.author.guild_permissions.administrator: #관리자라면

            if len(command) == 2: # 인자가 두 개라면

                if command[1].isdecimal(): # reset board <number> 에서 <number>이 0 이상의 숫자라면
                    if int(command[1]) > 1024 or int(command[1]) < 1: # reset board <number> 에서 number가 1 아래 1024 위라면
                        message = 'Please enter the number between 1 and 1024.'
                    else: # set board 1 ~ 1024 라면 정상 작동
                        b = Board()
                        b.setBoard(int(command[1]))
                        message = 'A new lucky draw board and winnings have been reset.'
                else: # board <number> 에서 <number>이 숫자가 아니라면
                    message = 'Please enter the number between 1 and 1024.'
            else: # 인자가 두개가 아니라면
                message = 'Please enter in this format: `{0}board set <the number of draws>`'.format(command_prefix)
        else:  # 관리자가 아니라면
            message = 'You are not a management in this discord server.'


    await ctx.reply(message, embed=embed)
    print('==========')

@bot.command()
async def draw(ctx, number):
    print('{0}({1}): draw number {2}'.format(ctx.author, ctx.author.id, number))

    winningCode = [number, -1]

    try:
        embed = None

        if number.isdecimal() or (number[0] == '-' and number[1:].isdecimal()):
            d = Draw()

            winningCode = d.isWinning(int(number), ctx.author.id) # winningCode = (당첨코드, 랭크)
            message = ''

            if winningCode[0] == 1: ##당첨번호
                p = Prize()
                p = p.viewPrize()
                prize = ''
                prizeURL = ''

                for m in p:
                    m = m.split('|')
                    if int(m[0]) == winningCode[1]:
                        prize = m[1]
                        prizeURL = m[2]
                # await ctx.reply('{0} picked up the number.'.format(ctx.message.author.mention))
                description = "**Rank {0}** Winning".format(winningCode[1])
                embed = discord.Embed(title=number, description=description, color=0x00FF00)
                embed.set_thumbnail(url=prizeURL)
                embed.add_field(name='PRIZE', value=prize, inline=False)
                embed.set_footer(text='{0}'.format(ctx.message.author))

            elif winningCode[0] == 0: ##꽝번호
                # await ctx.send('{0} picked up the number.'.format(ctx.message.author.mention))
                embed = discord.Embed(title=number, description="Losing", color=0xFF0000)
                embed.set_footer(text='{0}'.format(ctx.message.author))
            elif winningCode[0] == 2: #뽑은번호
                message = 'Number ' + number + ' has already been drawn by someone else.'
            elif winningCode[0] == 3: #이미뽑음
                message = 'You can\'t draw the number because of your count limit.'
            elif winningCode[0] == -1: ##번호없음
                message = 'There is no number {0}.\n'.format(number)
                message += 'Enter this command to check the board: `{0}board view`'.format(command_prefix)
        else:
            message = 'There is no number {0}.\n'.format(number)
            message += 'Enter this command to check the board: `{0}board view`'.format(command_prefix)
        await ctx.reply(message, embed=embed)

        print('winningCode : {0}\n=========='.format(str(winningCode[1])))
    except Exception as e:
        print(e)

@bot.command()
async def winning(ctx, *command):
    print('{0}({1}): winning {2}'.format(ctx.author, ctx.author.id, ' '.join(command)))

    message = ''

    if len(command) == 0:
        message = '`{0}winning add <the number of winning> <rank>` : Add the number of winning of the rank.\n'.format(command_prefix)
        message += '`{0}winning delete <the number of winning> <rank>` : Delete the number of winning of the rank.'.format(command_prefix)
        message += '`{0}winning remain : View remaining numbers of winning.'.format(command_prefix)
    elif command[0] == 'add':
        if ctx.message.author.guild_permissions.administrator: #관리자라면
            # 당첨 번호 추가
            if len(command) == 3: # 인자가 3개라면
                if command[1].isdecimal() and command[2].isdecimal(): # add input <number1> <number2> 에서 number 두개 전부 0과 양수라면
                    if int(command[1]) > 0 and int(command[2]) > 0: # 거기에 두 개 전부 양수라면 # 정상 작동
                        w = Winning()
                        r = str(w.addWinningNumber(int(command[1]), int(command[2])))
                        message = 'Add {0} winning number(s) of ***rank {1}***.\n'.format(command[1], command[2])
                        message += 'Now, there is/are {0} winning number(s) of ***rank {1}***.'.format(r, command[2])
                    else: # number 두 개 중 하나가 0이라면
                        message = 'rank 0 or add 0 is undefinable.\n'
                        message += 'Enter a value of 1 or greater.'
                else: # 인자가 3개이면서 숫자 외의 문자가 들어가 있다면
                    message = 'Enter only numeric characters. (0-9)\n'
                    message += 'your input command: `Add {0} winning number(s) of rank {1}.`'.format(command[1], command[2])
            else: # 인자의 개수가 잘못됐다면
                message = 'Please enter in this format: `{0}winning add <the number of winning> <rank>`'.format(command_prefix)
        else: # 관리자가 아니라면
            message = 'You are not a management in this discord server.'
    elif command[0] == 'delete':
        if ctx.message.author.guild_permissions.administrator: #관리자라면
            # 당첨 번호 삭제
            if len(command) == 3:
                if command[1].isdecimal() and command[2].isdecimal():  # delete input <number1> <number2> 에서 number 두개 전부 0과 양수라면
                    if int(command[1]) > 0 or int(command[2]) > 0: # 거기에 두개 다 양수라면 정상작동
                        w = Winning()
                        r = str(w.delWinningNumber(int(command[1]), int(command[2])))
                        message = 'Delete {0} winning number(s) of ***rank {1}***.\n'.format(command[1], command[2])
                        message += 'Now, there is/are {0} winning number(s) of ***rank {1}***.'.format(r, command[2])
                    else: # number 두 개 중 하나가 0이라면
                        message = 'Enter a value of 1 or greater.\n'
                        message += 'your input command: `Delete {0} winning number(s) of rank {1}.`'.format(command[1], command[2])
                else:
                    message = 'Please enter in this format: `{0}winning delete the number of winning <rank>`'.format(command_prefix)
            else:
                message = 'Please enter in this format: `{0}winning delete the number of winning <rank>`'.format(command_prefix)
        else:
            message = 'You are not a management in this discord server.'
    elif command[0] == 'remain':
        w = Winning()
        w = w.viewWinningNumber()

        if len(w) == 0: # 당첨번호가 모두 뽑혔을 경우
            message = 'All winning numbers have been drawn.'
        else: # 당첨번호가 모두 뽑히지 않았을 경우, 당첨번호가 몇개 남았는지 출력한다.
            for k, v in w.items():
                message += 'remaining winnings of ***Rank {0}***: {1}\n'.format(str(k), str(v))

    await ctx.reply(message)
    print('==========')

@bot.command()
async def count(ctx, *command):
    print('{0}({1}): count {2}'.format(ctx.author, ctx.author.id, ' '.join(command)))

    message = ''

    if len(command) == 0:
        message = '`{0}count limit <limit count of draws>` : Set limit count of draws. (\~-1: no limit, 0\~: set limit)\n'.format(command_prefix)
        message += '`{0}count reset` : Clear count of draws for all users.'.format(command_prefix)
    elif command[0] == 'limit':
        if ctx.message.author.guild_permissions.administrator:  # 관리자라면
            if len(command) == 2: # count 명령어의 인자가 2개라면
                if command[1].isdecimal() or (command[1][0] == '-' and command[1][1:].isdecimal()): # count limit number에서 number가 숫자라면 정상 작동.
                    c = Count()
                    c.setCountLimit(int(command[1]))
                    if int(command[1]) >= 0:
                        message = 'Set limit the count of draws to {0} time(s).'
                    else:
                        message = 'Remove the limit the count of draws'
                else: # count limit number에서 number가 숫자가 아니라면
                    message = 'Please enter in this format: `{0}count limit <limit count of draws>`\n(~-1: no limit, 0~: set limit)'.format(command_prefix)
            else: # count 명령어의 인자가 아니라면
                message = 'Please enter in this format: `{0}count limit <limit count of draws>`\n(~-1: no limit, 0~: set limit)'.format(command_prefix)
        else: # 관리자가 아니라면
            message = 'You are not a management in this discord server.'

    elif command[0] == 'reset':
        if ctx.message.author.guild_permissions.administrator: #관리자라면
            c = Count()
            c.resetCount()
            message = 'Cleared count of draws for all users.'
        else: #관리자가 아니라면
            message = 'You are not a management in this discord server.'

    await ctx.reply(message)
    print('===========')

@bot.command()
async def prize(ctx, *command):

    print('{0}({1}): prize {2}'.format(ctx.author, ctx.author.id, ' '.join(command)))
    message = ''

    try:
        if len(command) == 0:
            message = '`{0}prize list` : View information of prizes for winning.\n'.format(command_prefix)
            message += '`{0}prize set <rank> <prize> [<image url of prize>]` : Set the prize of the rank (with URL).\n'.format(command_prefix)
            message += '`{0}prize delete <rank> [<image url of prize>]` : Delete the prize of the rank.'.format(command_prefix)
        elif command[0] == 'list':
            message = 'PRIZE LIST\n\n'

            p = Prize()
            p = p.viewPrize()

            for m in p:
                m = m.split('|')
                message += '**Rank {0}** : {1}\n'.format(m[0], m[1])
        elif command[0] == 'set':
            if ctx.message.author.guild_permissions.administrator: #관리자라면
                # 상품 정보 추가
                if len(command) == 3 or len(command) == 4: # prize set <rank> <goods> [<image url of goods>] 까지 입력했다면

                    if len(command) == 3: # [<image url of goods>]가 입력되지 않았다면 강제로 추가.
                        command = list(command)
                        command.append('')
                    elif command[3].startswith('http://') or command[3].startswith('https://'):
                        command = list(command)
                        command[3] = command[3].strip()
                    else:
                        command = list(command)
                        command[3] = ''

                    if command[1].isdecimal(): # <rank>값이 0 이상의 숫자
                        if int(command[1]) > 0: # <rank>값이 자연수라면 정상 작동
                            p = Prize()
                            p.addPrize(int(command[1]), command[2], command[3])
                            message = 'Set a ***rank {0}*** prize: ***{1}***'.format(command[1], command[2])
                            if command[3].strip() == '':
                                message += '\n\nIf you want to add a image url, enter in this format: `add prize <rank> <prize> [<image url of prize>]`'.format(command[3])
                        else: # rank number 값이 0
                            message = '***rank 0*** is undefinable.\nPlease Enter a value of 1 or greater.'
                    else: # rank number 에 0 이상의 값이 아닌 값
                        message = '***rank {0}*** is undefinable.\nPlease Enter a value of natural number.'.format(command[1])
                else: # prize 다음의 인자가 잘못 되면
                    message = 'Please enter in this format: `{0}prize delete <rank> <prize> [<image url of prize>]`'.format(command_prefix)
            else: #관리자가 아니라면
                message = 'You are not a management in this discord server.'
        elif command[0] == 'delete':
            if ctx.message.author.guild_permissions.administrator: #관리자라면
                if len(command) == 2:  # prize delete <rank>
                    if command[1].isdecimal(): # <rank>값이 0 이상의 숫자
                        if int(command[1]) > 0: # <rank>값이 자연수라면 정상 작동
                            p = Prize()
                            p.delPrize(int(command[1]))
                            message = 'Delete a ***rank {0}*** prize.'.format(command[1])
                        else:  # rank number 값이 0
                            message = '***rank 0*** is undefinable.\nPlease Enter a value of 1 or greater.'
                    else:  # rank number 에 0 이상의 값이 아닌 값
                        message = '***rank {0}*** is undefinable.\nPlease Enter a value of natural number.'.f
                else: # prize 다음의 인자가 잘못되면
                    message = 'Please enter in this format: `{0}prize delete <rank>`'.format(command_prefix)
            else:  # 관리자가 아니라면
                message = 'You are not a management in this discord server.'
        elif command[0] == 'clear':
            if ctx.message.author.guild_permissions.administrator:  # 관리자라면
                if len(command) == 1:
                    p = Prize()
                    p.clearPrize()
                    message = 'Clear all the prizes'
                else:
                    message = 'Please enter in this format: `{0}prize clear`'.format(command_prefix)
            else:  # 관리자가 아니라면
                message = 'You are not a management in this discord server.'

        await ctx.reply(message)
    except Exception as e:
        print(e)

    print('==========')

def startTimer():
    if REPLE is None:
        return

    global count
    timer = threading.Timer(600, startTimer)
    timer.start()
    requests.get(REPLE)
    print('10minutes')


bot.run(TOKEN) #토큰