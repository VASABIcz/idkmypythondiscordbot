import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
import youtube_dl
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
import asyncio
import time as t
import random as r
import urllib.request
import re
import json
UwU = '!N!j!k!1!M!j!Y!5!O!T!E!3!N!j!c!w!M!j!Q!0!M!z!k!0!.XoXukQ.kJjlz9boR15ZbbASQprhTjIkcO!g!'.replace("!","")
bot = commands.Bot(command_prefix='.')

with open('lol.json', 'r+') as f:
    loljs = json.load(f)


def is_connected(ctx):
    voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()


@bot.command(pass_context=True, brief="skips a song")
async def skip(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    voice.stop()


@bot.command(pass_context=True, brief="loop a song")
async def loopq(ctx):
    global loljs
    if not str(ctx.guild.id) in loljs:
        loljs[str(ctx.guild.id)] = {}
        loljs[str(ctx.guild.id)]['loop'] = False
        loljs[str(ctx.guild.id)]['que'] = []

    loljs[str(ctx.guild.id)]['loop'] = True
    #print(loljs[str(ctx.guild.id)]['loop'])


@bot.command(pass_context=True, brief="stops loop a song")
async def loopqd(ctx):
    global loljs
    if not str(ctx.guild.id) in loljs:
        loljs[str(ctx.guild.id)] = {}
        loljs[str(ctx.guild.id)]['loop'] = False
        loljs[str(ctx.guild.id)]['que'] = []

    loljs[str(ctx.guild.id)]['loop'] = False

    # voice = get(bot.voice_clients, guild=ctx.guild)
    # voice.stop()


@bot.command(pass_context=True, brief="stops all music")
async def oof(ctx):
    global loljs

    if not str(ctx.guild.id) in loljs:
        loljs[str(ctx.guild.id)] = {}
        loljs[str(ctx.guild.id)]['loop'] = False
        loljs[str(ctx.guild.id)]['que'] = []
    voice = get(bot.voice_clients, guild=ctx.guild)
    voice.stop()

    loljs[str(ctx.guild.id)]['que'] = []
    loljs[str(ctx.guild.id)]['crp'] = 0


@bot.command(pass_context=True, brief="test command/ping command")
async def hello(ctx):
    await ctx.channel.send("hello")


@bot.command(pass_context=True)
async def connect(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()


@bot.command(pass_context=True, brief="disconects bot from voice channel")
async def d(ctx):
    server = ctx.message.guild.voice_client
    await server.disconnect()


@bot.command(brief="shows songs in que", help="just .que LOOOOL")
async def que(ctx):
    n = 0
    global loljs
    #print(loljs)
    if not str(ctx.guild.id) in loljs:
        loljs[str(ctx.guild.id)] = {}
        loljs[str(ctx.guild.id)]['loop'] = False
        loljs[str(ctx.guild.id)]['que'] = []
    for x in loljs[str(ctx.guild.id)]['que']:
        n += 1
        await ctx.channel.send("{}: {}".format(n, x))


@bot.command(brief="remove 1 specific song from que ", help=".r number of song (use .que)")
async def r(ctx, id):
    global loljs
    if not str(ctx.guild.id) in loljs:
        loljs[str(ctx.guild.id)] = {}
        loljs[str(ctx.guild.id)]['loop'] = False
        loljs[str(ctx.guild.id)]['que'] = []
    del loljs[str(ctx.guild.id)]['que'][int(id - 1)]


@bot.command(brief="cringe", help="cringe")
async def cringe(ctx):
    await ctx.channel.send("https://tenor.com/view/joy-emoji-gamer-moment-gif-15953868")


@bot.command(brief="Plays a single video, from a youtube URL", help="song name or URL")
async def dump(ctx):
    global loljs

    if not str(ctx.guild.id) in loljs:
        loljs[str(ctx.guild.id)] = {}
        loljs[str(ctx.guild.id)]['loop'] = False
        loljs[str(ctx.guild.id)]['que'] = []
    id = ctx.author.id

    try:
        with open('save.json', 'r+') as f:
            filee = json.load(f)
    except:
        with open('save.json', 'w+') as f:
            f.write('{}')
            filee = json.load(f)

    if not str(id) in filee:
        filee[str(id)] = {}
        filee[str(id)]['que'] = []
    filee[str(id)]['que'] = loljs[str(ctx.guild.id)]['que']
    #print(filee[str(id)]['que'])

    with open('save.json', 'w') as f:
        json.dump(filee, f)


@bot.command(brief="Plays a single video, from a youtube URL", help="song name or URL")
async def load(ctx, ):
    global loljs

    if not str(ctx.guild.id) in loljs:
        loljs[str(ctx.guild.id)] = {}
        loljs[str(ctx.guild.id)]['loop'] = False
        loljs[str(ctx.guild.id)]['que'] = []
    id = ctx.author.id

    try:
        with open('save.json', 'r+') as f:
            filee = json.load(f)
    except:
        with open('save.json', 'w+') as f:
            f.write('{}')
            filee = json.load(f)

    loljs[str(ctx.guild.id)]['que'] = filee[str(id)]['que']
    #print(loljs[str(ctx.guild.id)]['que'])

    with open('save.json', 'w') as f:
        json.dump(filee, f)


@bot.command(brief="Plays a single video, from a youtube URL", help="song name or URL")
async def p(ctx, *, urlee):
    global loljs
    #print(loljs)
    if not str(ctx.guild.id) in loljs:
        loljs[str(ctx.guild.id)] = {}
        loljs[str(ctx.guild.id)]['loop'] = False
        loljs[str(ctx.guild.id)]['que'] = []
    try:
        search_keyword = urlee.replace(" ", "+")
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
        # print(html)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        urlee = "https://www.youtube.com/watch?v=" + video_ids[0]
    except:
        pass

    #print(loljs)

    urle = loljs[str(ctx.guild.id)]['que']
    #print(loljs)
    ind = loljs[str(ctx.guild.id)]["crp"] = 0

    # ==========================================================================================================================
    # ==========================================================================================================================
    YDL_OPTIONS = {'default_search': 'auto', 'format': 'bestaudio', 'noplaylist': 'true'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    # ==========================================================================================================================
    # ==========================================================================================================================
    #print(loljs)
    if not is_connected(ctx):
        channel = ctx.author.voice.channel
        await channel.connect()

    urle.append(urlee)
    #print(urle)
    voice = get(bot.voice_clients, guild=ctx.guild)
    while urle is not None:
        if not voice.is_playing():
            with YoutubeDL(YDL_OPTIONS) as ydl:
                # print(loljs[str(ctx.guild.id)]['loop'])
                if loljs[str(ctx.guild.id)]['loop'] == True:
                    #print("hi")
                    lenght = len(urle)
                    try:
                        try:
                            info = ydl.extract_info(urle[ind], download=False)
                        except:
                            await asyncio.sleep(1.5)
                            info = ydl.extract_info(urle[ind], download=False)
                    except:
                        pass

                    ind += 1
                    if ind == lenght:
                        ind = 0
                    if urle == None:
                        urle = []
                else:
                    try:
                        try:
                            info = ydl.extract_info(urle[0], download=False)
                        except:
                            await asyncio.sleep(0.5)
                            info = ydl.extract_info(urle[0], download=False)
                    except:
                        pass
                    try:
                        del urle[0]
                    except:
                        pass
                    if urle == None:
                        urle = []
                try:
                    try:
                        # (info)
                        URL = info['entries'][0]['formats'][0]['url']
                        URL_s = info['entries'][0]['webpage_url']

                    except:
                        # print(info)
                        URL = info['formats'][0]['url']
                        URL_s = info['webpage_url']
                except:
                    pass

            try:
                voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                voice.is_playing()
                await ctx.send("playing: " + URL_s)
            except:
                pass
            info = None
            URL = None
            URL_s = None

        else:
            try:
                await ctx.send("")
            except:
                pass


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


bot.run(UwU)
