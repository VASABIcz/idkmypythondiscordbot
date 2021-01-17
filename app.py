import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from os import listdir
from constant import *

# TODO Checks guild only ...
#
# known bugs
# ¯\_(ツ)_/¯
# TODO per guild prefix



load_dotenv('.env')
PREF = os.environ['PREF']
TOKEN = os.environ['TOKEN']
bot = commands.Bot(command_prefix=PREF)


@bot.command(brief="reload cogs")
@commands.is_owner()
async def reload(ctx, name):
    bot.reload_extension(f'cogs.{name}')
    await ctx.channel.send('cog reloaded')


@bot.command(brief="simple eval", name='eval')
@commands.is_owner()
async def evale(ctx, *, eve):
    evee = (str(eval(eve)))
    await ctx.channel.send(evee)



@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {bot.latency}')


@bot.event
async def on_command_error(ctx, error):
    webhook = DiscordWebhook(
        url='https://discord.com/api/webhooks/797142718777262121/ciIaNQ-hBMIS9ZGbCCpPoDSTT1lvKQukYy4RIJTtxKB3Ue9k_RIvh-FFAR1sUKk6ooaV',
        content=f'{ctx.author} \n {ctx.guild} \n {str(error)}')
    response = webhook.execute()


###NAPISE KDYZ JE BOT PRIPRAVEN K POUZIVANI
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('---------------------')
    activity = discord.Game(name=f"{PREF}help")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    files = listdir('cogs')
    for n in files:
        if n != '__pycache__':
            if not '#' in n:
                bot.load_extension(f'cogs.{n.replace(".py", "")}')


###DISCORD BOT TOKEN
bot.run(TOKEN)
