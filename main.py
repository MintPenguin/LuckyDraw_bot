#run.py
import discord
from discord.ext import commands
from fileGenerator import *
from number import *
import threading
import requests
#import sys

TOKEN = os.environ.get('LUCKY_DRAW_TOKEN')
HEROKU = os.environ.get('HEROKU_DOMAIN')
bot = discord.Client()
bot = commands.Bot(command_prefix="##")

@bot.event
async def on_ready():
#    print(sys.executable)
    startTimer()
    numberRun()
    print('We have logged in as {0.user}'.format(bot)) #봇이 실행되면 콘솔창에 표시

@bot.event
async def on_command_error(ctx, error):
    return
#    if isinstance(error, commands.CommandNotFound):
#    	await ctx.send("command not found")

@bot.command()
async def draw(ctx, number):
    winningCode = isWinning(number, ctx.author.id)
    if winningCode == 1: ##당첨번호
        await ctx.send('{0} picked up the number.'.format(ctx.message.author.mention))
        embed = discord.Embed(title=number, description="winning", color=0x00FF00)
        embed.set_footer(text = '{0}'.format(ctx.message.author.name))
        await ctx.send(embed = embed)
    elif winningCode == 0: ##꽝번호
        await ctx.send('{0} picked up the number.'.format(ctx.message.author.mention))
        embed = discord.Embed(title=number, description="losing", color=0xFF0000)
        embed.set_footer(text='{0}'.format(ctx.message.author.name))
        await ctx.send(embed = embed)
    elif winningCode == 2: #뽑은번호
        await ctx.send(number + ' has already been picked up.')
    elif winningCode == 3: #뽑음
        await ctx.send('You have already drawn a number.')
    elif winningCode == -1: ##번호없음
        None

    print('{0} picked up the number.'.format(ctx.message.author.mention))
    print('winningCode : {0}'.format(str(winningCode)))

@bot.command()
async def remain(ctx):

    text = ''
    numberList = remainingNumber()

    for nl in numberList:
        text += str(nl) + ' '

    embed = discord.Embed(title="remaining numbers", description=text, color=0x808080)
    await ctx.send(embed = embed)

    print('remain')

@bot.command()
async def set(ctx, command1, command2):
    if ctx.guild:
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.send('You are not a management in this discord server.')
            return

    if command1 == 'last':
        setLastNumber(command2)
        await ctx.send('set a new lucky draw.')
    if command1 == 'count':
        setlimitTimes(command2)
        await ctx.send('set a count.')

    print('set', command1, command2)

@bot.command()
async def clear(ctx, command1):
    if ctx.guild:
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.send('You are not a management in this discord server.')
            return

    if command1 == 'count':
        fileClear(nickNameFile)
        await ctx.send('Reset count.')

    pritn('clear', command1)

def startTimer():
    global count
    timer = threading.Timer(600, startTimer)
    timer.start()
    requests.get(HEROKU)
    print('10minutes')


bot.run(TOKEN) #토큰