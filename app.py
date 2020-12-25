import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
import json
import asyncio
import random as re

###LOAD OPUS USED FOR RUNNING ON SERVER
discord.opus.load_opus()
bot = commands.Bot(command_prefix='.')

loljs = {}


def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb


def init(ctx):
    global loljs
    if not str(ctx.guild.id) in loljs:
        loljs[str(ctx.guild.id)] = {}
        loljs[str(ctx.guild.id)]['loop'] = False
        loljs[str(ctx.guild.id)]['que'] = []
        loljs[str(ctx.guild.id)]["crp"] = 0
        loljs[str(ctx.guild.id)]["crpe"] = {}
        loljs[str(ctx.guild.id)]["crpe"]['tit'] = None
        loljs[str(ctx.guild.id)]["crpe"]['URL_s'] = None
        loljs[str(ctx.guild.id)]["crpe"]['thumb'] = None


def is_connected(ctx):
    voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()


@bot.command(brief="skips a song")
async def skip(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice is not None:
        voice.stop()
        await ctx.send("song has been skiped (:")
    else:
        await ctx.send("nothing to skip (((((((((:")


@bot.command(brief="loop a song")
async def loopq(ctx):
    global loljs
    init(ctx)

    loljs[str(ctx.guild.id)]['loop'] = True
    await ctx.send("que has been looped (:")




@bot.command(brief="stops loop a song")
async def loopqd(ctx):
    global loljs
    init(ctx)

    loljs[str(ctx.guild.id)]['loop'] = False
    await ctx.send("que has been un looped (:")


@bot.command(brief="stops all music")
async def oof(ctx):
    global loljs
    voice = get(bot.voice_clients, guild=ctx.guild)
    init(ctx)
    loljs[str(ctx.guild.id)]['que'] = []
    loljs[str(ctx.guild.id)]['crp'] = 0
    if voice:
        if voice.is_playing():
            voice.stop()
            await ctx.send("U have succesfully oofed the bot")


@bot.command(brief="test command/ping command")
async def hello(ctx):
    await ctx.channel.send("hello")


@bot.command(brief="...")
async def connect(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()


@bot.command(brief="disconects bot from voice channel")
async def d(ctx):
    server = ctx.message.guild.voice_client
    await server.disconnect()
    await ctx.send("U DcD me D:")


@bot.command(brief="shows songs in que", help="just .que LOOOOL")
async def que(ctx, nam=0):
    global loljs
    init(ctx)
    nam = int(nam)
    n = 0

    if nam == 0:
        pass
    else:
        n = (nam * 5) - 5

    qee = loljs[str(ctx.guild.id)]['que']

    embed = discord.Embed(title="QUE (:", description="Song que", colour=discord.Colour.from_rgb(re.randrange(0, 255), 0, re.randrange(0, 255)))
    embed.set_author(name='VASABI',
                     url='https://github.com/VASABIcz/Simple-discord-music-bot',           
                     icon_url='https://i.ytimg.com/vi_webp/xeA7VQE_R1k/maxresdefault.webp')
    for i in range(5):
        try:
            embed.add_field(name=qee[int(i + n)]['tit'], value=str(i + 1 + n), inline=False)
        except:
            pass

    embed.set_footer(text="page<{}>".format(nam))
    await ctx.send(embed=embed)


@bot.command(brief="remove 1 specific song from que ", help=".r number of song (use .que)")
async def r(ctx, *, id=None):
    if id:
        if isinstance(id, int):
            if id <= 0:
                global loljs
                init(ctx)
                if len(loljs[str(ctx.guild.id)]['que']) >= id - 1:
                    del loljs[str(ctx.guild.id)]['que'][int(id - 1)]
                    await ctx.send(
                        "{} has been removed from que".format(loljs[str(ctx.guild.id)]['que'][int(id - 1)]['tit']))
                else:
                    await ctx.send('Bad ID')
            else:
                await ctx.send('Bad ID')
        else:
            await ctx.send('Bad ID')
    else:
        await ctx.send('U need to add number of song in que (:')



@bot.command(brief="cringe", help="cringe")
async def cringe(ctx):
    await ctx.channel.send("https://im.ezgif.com/tmp/ezgif-1-37968d44d448.gif")


@bot.command(brief="nya", help="nya")
async def nya(ctx):
    await ctx.channel.send("https://im.ezgif.com/tmp/ezgif-1-37968d44d448.gif")


@bot.command(brief="Plays a single video, from a youtube URL", help="song name or URL")
async def dump(ctx):
    global loljs
    init(ctx)
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
async def load(ctx):
    global loljs
    idd = ctx.author.id

    init(ctx)

    try:
        with open('save.json', 'r+') as f:
            filee = json.load(f)
    except:
        with open('save.json', 'w+') as f:
            f.write('{}')
            filee = json.load(f)

    loljs[str(ctx.guild.id)]['que'] = filee[str(idd)]['que']

    if not filee[str(idd)]['que']:
        await ctx.send("U didnt save any que D:")
    else:
        qoe = loljs[str(ctx.guild.id)]['que'][0]['URL_s']
        #del loljs[str(ctx.guild.id)]['que'][0]
        await ctx.invoke(bot.get_command('p'), urlee=qoe)


@bot.command(brief="Plays a single video, from a youtube URL", help="song name or URL")
async def play(ctx, *, urlee=None):
    await ctx.invoke(bot.get_command('p'), urlee=urlee)


@bot.command(brief="Plays a single video, from a youtube URL", help="song name or URL")
async def crp(ctx):
    init(ctx)
    global loljs
    if loljs[str(ctx.guild.id)]["crpe"]['tit'] != None:
        tit = loljs[str(ctx.guild.id)]["crpe"]['tit']
        URL_s = loljs[str(ctx.guild.id)]["crpe"]['URL_s']
        thumb = loljs[str(ctx.guild.id)]["crpe"]['thumb']
        embed = discord.Embed(title=tit, url=URL_s, description='Currently playing',
                              colour=discord.Colour.from_rgb(re.randrange(0, 255), 0, re.randrange(0, 255)))
        embed.set_author(name='VASABI', url='https://github.com/VASABIcz/Simple-discord-music-bot',
                         icon_url='https://i.ytimg.com/vi_webp/xeA7VQE_R1k/maxresdefault.webp')
        embed.set_thumbnail(url=thumb)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Nothing is playing")


@bot.command(brief="Plays a single video, from a youtube URL", help="song name or URL")
async def p(ctx, *, urlee=None):
    if urlee is None:
        await ctx.send(" U need to give a song name or URL (:")
    else:
        global loljs

        ###INITS SERVER
        init(ctx)

        ###YTDL FFMPEG SETTINGS
        # ==========================================================================================================================
        # ==========================================================================================================================
        # YDL_OPTIONS = {'default_search': 'auto', 'format': 'bestaudio', 'noplaylist': 'true', 'quiet': 'true'}
        YDL_OPTIONS = {'format': 'bestaudio/best',
                       'restrictfilenames': True,
                       'noplaylist': True,
                       'nocheckcertificate': True,
                       'ignoreerrors': False,
                       'logtostderr': False,
                       'quiet': True,
                       'no_warnings': False,
                       'default_search': 'auto',
                       'source_address': '0.0.0.0'}

        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                          'options': '-vn'}
        # ==========================================================================================================================
        # ==========================================================================================================================

        ###CONNECTS TO VOICE CHANNEL
        if ctx.author.voice is None:
            await ctx.send("Ur not connected to voice channel")
        else:
            if not is_connected(ctx):
                channel = ctx.author.voice.channel
                await channel.connect()
            voice = get(bot.voice_clients, guild=ctx.guild)

            ###INIT YTDL
            with YoutubeDL(YDL_OPTIONS) as ydl:

                ###HANDLE PLAYLIST/VIDEOS
                try:
                    info = ydl.extract_info(urlee, download=False)
                    if 'entries' in info and info['entries'] == []:
                        await ctx.send("BAD")
                    else:
                        if 'youtube.com/playlist?list=' in urlee:
                            for i in range(len(info['entries'])):
                                print(i)
                                loljs[str(ctx.guild.id)]['que'].append({})
                                thumb = loljs[str(ctx.guild.id)]['que'][len(loljs[str(ctx.guild.id)]['que']) - 1]['thumb'] = info['entries'][i]['thumbnail']
                                loljs[str(ctx.guild.id)]['que'][len(loljs[str(ctx.guild.id)]['que']) - 1]['URl'] = info['entries'][i]['url']
                                URL_s = loljs[str(ctx.guild.id)]['que'][len(loljs[str(ctx.guild.id)]['que']) - 1]['URL_s'] = info['entries'][i]['webpage_url']
                                tit = loljs[str(ctx.guild.id)]['que'][len(loljs[str(ctx.guild.id)]['que']) - 1]['tit'] = info['entries'][i]['title']
                        else:
                            if 'entries' not in info:
                                loljs[str(ctx.guild.id)]['que'].append({})
                                thumb = loljs[str(ctx.guild.id)]['que'][len(loljs[str(ctx.guild.id)]['que']) - 1]['thumb'] = info['thumbnail']
                                loljs[str(ctx.guild.id)]['que'][len(loljs[str(ctx.guild.id)]['que']) - 1]['URl'] = info['url']
                                URL_s = loljs[str(ctx.guild.id)]['que'][len(loljs[str(ctx.guild.id)]['que']) - 1]['URL_s'] = info['webpage_url']
                                loljs[str(ctx.guild.id)]['que'][len(loljs[str(ctx.guild.id)]['que']) - 1]['tit'] = info['title']
                            else:
                                loljs[str(ctx.guild.id)]['que'].append({})
                                thumb = loljs[str(ctx.guild.id)]['que'][len(loljs[str(ctx.guild.id)]['que']) - 1]['thumb'] = info['entries'][0]['thumbnail']
                                loljs[str(ctx.guild.id)]['que'][len(loljs[str(ctx.guild.id)]['que']) - 1]['URl'] = info['entries'][0]['url']
                                URL_s = loljs[str(ctx.guild.id)]['que'][len(loljs[str(ctx.guild.id)]['que']) - 1]['URL_s'] = info['entries'][0]['webpage_url']
                                tit = loljs[str(ctx.guild.id)]['que'][len(loljs[str(ctx.guild.id)]['que']) - 1]['tit'] = info['entries'][0]['title']

                        ###SEND EMBED
                        embed = discord.Embed(title=tit,
                                              url=URL_s,
                                              description='Added to que:',
                                              colour=discord.Colour.from_rgb(re.randrange(0, 255), 0,
                                                                             re.randrange(0, 255)))

                        embed.set_author(name='VASABI',
                                         url='https://github.com/VASABIcz/Simple-discord-music-bot',
                                         icon_url='https://i.ytimg.com/vi_webp/xeA7VQE_R1k/maxresdefault.webp')

                        embed.set_thumbnail(url=thumb)

                        if loljs[str(ctx.guild.id)]["crpe"]['tit']:
                            embed.set_footer(text="Position in que: {}".format(len(loljs[str(ctx.guild.id)]['que'])))
                        else:
                            if loljs[str(ctx.guild.id)]['loop']:
                                embed.set_footer(
                                    text="Position in que: {}".format(len(loljs[str(ctx.guild.id)]['que'])))
                            else:
                                embed.set_footer(text="Now playing")
                        await ctx.send(embed=embed)

                except:
                    await ctx.send("BAD URL D:")
                    ###SOME LOOP AND INIT STUFF
                while True:
                    if not voice.is_playing():
                        if loljs[str(ctx.guild.id)]['que']:
                            loop = loljs[str(ctx.guild.id)]['loop']

                            ###EXTRACT FROM JSON
                            thumb = loljs[str(ctx.guild.id)]['que'][loljs[str(ctx.guild.id)]["crp"]]['thumb']
                            URL = loljs[str(ctx.guild.id)]['que'][loljs[str(ctx.guild.id)]["crp"]]['URl']
                            URL_s = loljs[str(ctx.guild.id)]['que'][loljs[str(ctx.guild.id)]["crp"]]['URL_s']
                            tit = loljs[str(ctx.guild.id)]['que'][loljs[str(ctx.guild.id)]["crp"]]['tit']
                            loljs[str(ctx.guild.id)]["crpe"]['tit'] = tit
                            loljs[str(ctx.guild.id)]["crpe"]['URL_s'] = URL_s
                            loljs[str(ctx.guild.id)]["crpe"]['thumb'] = thumb

                            ###HANDLE LOOP
                            if loop:
                                lenght = len(loljs[str(ctx.guild.id)]['que'])
                                loljs[str(ctx.guild.id)]["crp"] += 1
                                if loljs[str(ctx.guild.id)]["crp"] == lenght:
                                    loljs[str(ctx.guild.id)]["crp"] = 0
                            else:
                                del loljs[str(ctx.guild.id)]['que'][0]

                            ###STREAM AUDIO
                            voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                            voice.source = discord.PCMVolumeTransformer(voice.source)
                            voice.source.volume = 0.01
                            voice.is_playing()

                            ###SOME BULLSHIT THAT MAKES IT WORK THIS MIGHT BE BETTER
                            await asyncio.sleep(1)
                        else:
                            loljs[str(ctx.guild.id)]["crpe"]['tit'] = None
                            loljs[str(ctx.guild.id)]["crpe"]['URL_s'] = None
                            loljs[str(ctx.guild.id)]["crpe"]['thumb'] = None
                            await asyncio.sleep(1)
                    else:
                        await asyncio.sleep(1)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('---------------------')
    activity = discord.Game(name=".help")
    await bot.change_presence(status=discord.Status.online, activity=activity)


bot.run('Njk1MjY5OTE3NjcwMjQ0Mzk0.XoXukQ.kJjlz9boR15ZbbASQprhTjIkcOg')
