import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from discord_webhook import DiscordWebhook
from constant import *


load_dotenv('.env')
PREF = os.environ['PREF']
TOKEN = os.environ['TOKEN']
bot = commands.Bot(command_prefix=PREF)


@bot.command()
@commands.is_owner()
async def reload(ctx, name):
    bot.reload_extension(f'cogs.{name}')
    await ctx.channel.send('cog reloaded')


@bot.command()
@commands.is_owner()
async def eval(ctx, *, eve):
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
    bot.load_extension('cogs.music')





###DISCORD BOT TOKEN
bot.run(TOKEN)
