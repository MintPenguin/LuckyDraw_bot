#run.py
import discord
from discord.ext import commands
from fileGenerator import *
from number import *
import threading, requests
#import sys

TOKEN = os.environ.get('LUCKY_DRAW_TOKEN')
HEROKU = os.environ.get('HEROKU_DOMAIN') # for free tier at heroku
bot = discord.Client()
bot = commands.Bot(command_prefix="##")

@bot.event
async def on_ready():
#    print(sys.executable)
    startTimer()
    numberRun()
    print('We have logged in as {0.user}\n'.format(bot))

@bot.event
async def on_command_error(ctx, error):
#    return
    if isinstance(error, commands.CommandNotFound):
#    	await ctx.send("command not found")
        print(error)


print('{0}({1}): draw number {2}'.format(ctx.author, ctx.author.id, number))
@bot.command()
async def draw(ctx, number):

    winningCode = isWinning(number, ctx.author.id)
    if winningCode == 1: ##당첨번호
        # await ctx.reply('{0} picked up the number.'.format(ctx.message.author.mention))
        embed = discord.Embed(title=number, description="winning", color=0x00FF00)
        embed.set_footer(text = '{0}'.format(ctx.message.author))
        await ctx.reply(embed = embed)
    elif winningCode == 0: ##꽝번호
        # await ctx.send('{0} picked up the number.'.format(ctx.message.author.mention))
        embed = discord.Embed(title=number, description="losing", color=0xFF0000)
        embed.set_footer(text='{0}'.format(ctx.message.author))
        await ctx.reply(embed = embed)
    elif winningCode == 2: #뽑은번호
        await ctx.send(number + ' has already been picked up.')
    elif winningCode == 3: #이미뽑음
        await ctx.send('You have already drawn a number.')
    elif winningCode == -1: ##번호없음
        await ctx.send('There is no number.')

    print('winningCode : {0}\n'.format(str(winningCode)))

@bot.command()
async def remain(ctx):
    print('{0}({1}): remain'.format(ctx.author, ctx.author.id))

    text = ''
    numberList = remainingNumber()

    for nl in numberList:
        text += str(nl) + ' '

    embed = discord.Embed(title="remaining numbers: {0}".format(str(len(numberList))), description=text, color=0x808080)
    await ctx.send(embed = embed)

    print('\n')

@bot.command()
async def set(ctx, command1, command2):
    print('{0}({1}): set {2} {3}'.format(ctx.author, ctx.author.id, command1, command2))

    if ctx.guild:
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.reply('You are not a management in this discord server.')
            print('')
            return

    if command1 == 'last':
        if int(command2) > 1024 or int(command2) < 1:
            await ctx.reply('Please enter the last number between 1 and 1024.')
            print('')
            return
        setLastNumber(command2)
        await ctx.send('set a new lucky draw.')
    if command1 == 'count':
        setlimitTimes(command2)
        await ctx.send('set a count.')

    print('')

@bot.command()
async def clear(ctx, command1):
    if ctx.guild:
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.reply('You are not a management in this discord server.')
            print('')
            return

    if command1 == 'count':
        fileClear(nickNameFile)
        await ctx.send('Reset count.')

    print(ctx.author.id, ': clear', command1, '\n')

def startTimer():
    if HEROKU is None:
        return

    global count
    timer = threading.Timer(600, startTimer)
    timer.start()
    requests.get(HEROKU)
    print('10minutes')


bot.run(TOKEN) #토큰