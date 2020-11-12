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

#discord.opus.load_opus()

bot: Bot = commands.Bot(command_prefix='.')
with open('cache.json', 'r+') as f:
    cache = json.load(f)

loljs = {}




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
    


@bot.command(pass_context=True, brief="stops loop a song")
async def loopqd(ctx):
    global loljs
    if not str(ctx.guild.id) in loljs:
        loljs[str(ctx.guild.id)] = {}
        loljs[str(ctx.guild.id)]['loop'] = False
        loljs[str(ctx.guild.id)]['que'] = []

    loljs[str(ctx.guild.id)]['loop'] = False




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
async def que(ctx, nam):
    nam = int(nam)
    global loljs
    n = 0
    if nam == None:
        n = 0
    if nam == 1:
        n = 0
    if nam == 2:
        n = 5
    if nam == 3:
        n = 10
    if nam == 4:
        n = 15


    
    #if not str(ctx.guild.id) in loljs:
    #    loljs[str(ctx.guild.id)] = {}
    #    loljs[str(ctx.guild.id)]['loop'] = False
    #    loljs[str(ctx.guild.id)]['que'] = []
    #for x in loljs[str(ctx.guild.id)]['que']:
    #    n += 1
    #    await ctx.channel.send("{}: {}".format(n, x))


    qee = loljs[str(ctx.guild.id)]['que']

    embed = discord.Embed(title="QUE (:", description="Song que", color=0x00ff00)
    embed.set_author(name="VASABI", url="https://github.com/VASABIcz/idkmypythondiscordbot")

    try:
        embed.add_field(name=qee[0+n], value=1+n, inline=False)
    except:
        pass
    try:
        embed.add_field(name=qee[1+n], value=2+n, inline=False)
    except:
        pass
    try:
        embed.add_field(name=qee[2+n], value=3+n, inline=False)
    except:
        pass
    try:
        embed.add_field(name=qee[3+n], value=4+n, inline=False)
    except:
        pass
    try:
        embed.add_field(name=qee[4+n], value=5+n, inline=False)
    except:
        pass
    embed.set_footer(text="page<{}>".format(nam))
    await ctx.send(embed=embed)


@bot.command(brief="remove 1 specific song from que ", help=".r number of song (use .que)")
async def r(ctx, *, id):
    id = int(id)
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


    with open('save.json', 'w') as f:
        json.dump(filee, f)
    await ctx.invoke(bot.get_command('p'), urlee=None)

# TODO Bug fix
# TODO embed
# TODO link  cache DONE
# TODO make all extracrion on start ASI NE LIK SE SMAZE PO CASE
@bot.command(brief="Plays a single video, from a youtube URL", help="song name or URL")
async def p(ctx, *, urlee):
    global loljs
    global cache
    if not str(ctx.guild.id) in loljs:
        loljs[str(ctx.guild.id)] = {}
        loljs[str(ctx.guild.id)]['loop'] = False
        loljs[str(ctx.guild.id)]['que'] = []
    try:
        urleee = cache[str(urlee)]['Url']

    except:
        vid = urlee
        search_keyword = vid.replace(" ", "+")
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        urleee = "https://www.youtube.com/watch?v=" + video_ids[0]
        cache[str(urlee)] = {}
        cache[str(urlee)]['Url'] = str(urleee)
        with open('cache.json', 'w') as f:
            json.dump(cache, f)
    urleee = urlee


    urle = loljs[str(ctx.guild.id)]['que']
    ind = loljs[str(ctx.guild.id)]["crp"] = 0

    # ==========================================================================================================================
    # ==========================================================================================================================
    YDL_OPTIONS = {'default_search': 'auto', 'format': 'bestaudio', 'noplaylist': 'true'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    # ==========================================================================================================================
    # ==========================================================================================================================
    if not is_connected(ctx):
        channel = ctx.author.voice.channel
        await channel.connect()

    urle.append(urleee)
    voice = get(bot.voice_clients, guild=ctx.guild)
    while urle is not None:
        if not voice.is_playing():
            with YoutubeDL(YDL_OPTIONS) as ydl:
               
                if loljs[str(ctx.guild.id)]['loop'] == True:
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
                            await asyncio.sleep(1.5)
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

                        URL = info['entries'][0]['formats'][0]['url']
                        URL_s = info['entries'][0]['webpage_url']
                        tit = info['entries'][0]['title']
                        thumb = info['entries'][0]['thumbnails'][0]['url']

             

                    except:

                        URL = info['formats'][0]['url']
                        URL_s = info['webpage_url']
                        tit = info[0]['title']
                        thumb = info[0]['thumbnails'][0]['url']
                  
                except:
                    pass

            try:
                voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                voice.is_playing()
                #await ctx.send("playing: " + URL_s)


                #embedVar = discord.Embed(title="Now playing", description=URL_s, color=0x00ff00)
                #embedVar.add_field(name="Field1", value="hi", inline=False)
                #embedVar.add_field(name="Field2", value="hi2", inline=False)
                #await ctx.send(embed=embedVar)

                #22222222222222222222222222222222222222
                embed = discord.Embed(title=tit,
                                      url=URL_s, description="Now playing:",
                                      color=0x00ff00)
                embed.set_author(name="VASABI", url="https://github.com/VASABIcz/idkmypythondiscordbot")
                embed.set_thumbnail(
                    url=thumb)
                await ctx.send(embed=embed)


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


bot.run('Njk1MjY5OTE3NjcwMjQ0Mzk0.XoXukQ.kJjlz9boR15ZbbASQprhTjIkcOg!!!'.replace("!",""))
