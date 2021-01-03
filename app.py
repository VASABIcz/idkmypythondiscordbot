import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
import json
import asyncio
import random as re
import time

bot = commands.Bot(command_prefix='.')

loljs = {}


# TODO new HELP command
# TODO while moving bot que is None VALVE PLS FIX
# guse fixed duno
#TODO interactive command que
#FIXED

def init(ctx):
    global loljs
    if ctx.guild.id not in loljs:
        loljs[ctx.guild.id] = {}
        loljs[ctx.guild.id]['loop'] = False
        loljs[ctx.guild.id]['que'] = []
        loljs[ctx.guild.id]["crp"] = 0
        loljs[ctx.guild.id]['voice_id'] = None
        loljs[ctx.guild.id]["crpe"] = {}
        loljs[ctx.guild.id]["crpe"]['tit'] = None
        loljs[ctx.guild.id]["crpe"]['URL_s'] = None
        loljs[ctx.guild.id]["crpe"]['thumb'] = None
        loljs[ctx.guild.id]["crpe"]['URL'] = None
        loljs[ctx.guild.id]['mid'] = None
        loljs[ctx.guild.id]['ply'] = True
        loljs[ctx.guild.id]['rpm'] = {}
        loljs[ctx.guild.id]['rpm']['mid'] = None
        loljs[ctx.guild.id]['rpm']['chid'] = None
        loljs[ctx.guild.id]['quem'] = {}
        loljs[ctx.guild.id]['quem']['mid'] = None
        loljs[ctx.guild.id]['quem']['chid'] = None
        loljs[ctx.guild.id]['quem']['pg'] = None


def is_connected(ctx):
    voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()


def scrap(URL):
    x = URL.find('expire=')
    x += 7
    y = URL.find('&ei')
    ur = int(URL[x:y])
    ur += -600
    tim = time.time()
    if ur <= tim:
        return True
    else:
        return False


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

    loljs[ctx.guild.id]['loop'] = True
    await ctx.send("que has been looped (:")


@bot.command(brief="stops loop a song")
async def loopqd(ctx):
    global loljs
    init(ctx)

    loljs[ctx.guild.id]['loop'] = False
    await ctx.send("que has been un looped (:")


@bot.command(brief="stops all music")
async def oof(ctx):
    global loljs
    init(ctx)

    voice = get(bot.voice_clients, guild=ctx.guild)
    loljs[ctx.guild.id]['que'] = []
    loljs[ctx.guild.id]['crp'] = 0
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
async def que(ctx, nam=1):
    global loljs
    init(ctx)
    try:
        if loljs[ctx.guild.id]['quem']['chid'] is not None:
            chal = bot.get_channel(loljs[ctx.guild.id]['quem']['chid'])
            message = await chal.fetch_message(loljs[ctx.guild.id]['quem']['mid'])
            await message.delete()
    except:
        pass
    if nam < 1:
        nam = 1

    qee = loljs[ctx.guild.id]['que']
    embed = discord.Embed(title="QUE (:", description="Song que",colour=discord.Colour.from_rgb(re.randrange(0, 255), 0, re.randrange(0, 255)))
    embed.set_author(name='VASABI',url='https://github.com/VASABIcz/Simple-discord-music-bot',icon_url='https://i.ytimg.com/vi_webp/xeA7VQE_R1k/maxresdefault.webp')
    for i in range(5):
        try:
            embed.add_field(name=qee[int(i + (nam * 5) - 5)]['tit'], value=str(i + 1 + (nam * 5) - 5), inline=False)
        except:
            pass

    embed.set_footer(text="page<{}>".format(nam))
    message = await ctx.send(embed=embed)
    await message.add_reaction('◀️')
    await message.add_reaction('▶️')
    await message.add_reaction('🔄')
    await asyncio.sleep(1)
    loljs[ctx.guild.id]['quem']['mid'] = message.id
    loljs[ctx.guild.id]['quem']['chid'] = ctx.channel.id
    loljs[ctx.guild.id]['quem']['pg'] = nam


@bot.command(brief="remove 1 specific song from que ", help=".r number of song (use .que)")
async def r(ctx, *, id=None):
    if id:
        id = int(id)
        if isinstance(id, int):
            if id >= 0:
                global loljs
                init(ctx)
                if len(loljs[ctx.guild.id]['que']) >= id - 1:
                    del loljs[ctx.guild.id]['que'][int(id - 1)]
                    await ctx.send(
                        "{} has been removed from que".format(loljs[ctx.guild.id]['que'][int(id - 1)]['tit']))
                else:
                    await ctx.send('Bad ID')
            else:
                await ctx.send('Bad ID')
        else:
            await ctx.send('Bad ID')
    else:
        await ctx.send('U need to add number of song in que (:')


@bot.command(brief="shows songs in que", help="just .que LOOOOL")
async def q(ctx, nam=1):
    await ctx.invoke(bot.get_command('que'), nam=nam)


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
    filee[str(id)]['que'] = loljs[ctx.guild.id]['que']

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

    loljs[ctx.guild.id]['que'] = filee[str(idd)]['que']

    if not filee[str(idd)]['que']:
        await ctx.send("U didnt save any que D:")
    else:
        if loljs[ctx.guild.id]['que']:
            ###VALIDATE FIRST LINK/
                if scrap(loljs[ctx.guild.id]['que'][0]['URL']):
                    print('hmmeee')
                    YDL_OPTIONS = {'format': 'bestaudio/best',
                                   'restrictfilenames': True,
                                   'noplaylist': True,
                                   'nocheckcertificate': True,
                                   'ignoreerrors': True,
                                   'logtostderr': False,
                                   'quiet': True,
                                   'no_warnings': False,
                                   'default_search': 'auto',
                                   'source_address': '0.0.0.0'}
                    ydl = YoutubeDL(YDL_OPTIONS)
                    info = ydl.extract_info(loljs[ctx.guild.id]['que'][0]['URL_s'], download=False)
                    loljs[ctx.guild.id]['que'][0]['URL'] = info['url']
        # del loljs[ctx.guild.id]['que'][0]
        await ctx.invoke(bot.get_command('p'), urlee='')


@bot.command(brief="Plays a single video, from a youtube URL", help="song name or URL")
async def play(ctx, *, urlee=None):
    await ctx.invoke(bot.get_command('p'), urlee=urlee)


@bot.command(brief="Plays a single video, from a youtube URL", help="song name or URL")
async def crp(ctx):
    init(ctx)
    global loljs
    if loljs[ctx.guild.id]["crpe"]['tit'] is not None:
        try:
            if loljs[ctx.guild.id]['rpm']['chid'] is not None:
                chal = bot.get_channel(loljs[ctx.guild.id]['rpm']['chid'])
                message = await chal.fetch_message(loljs[ctx.guild.id]['rpm']['mid'])
                await message.delete()
        except:
            pass
        embed = discord.Embed(title=loljs[ctx.guild.id]["crpe"]['tit'], url=loljs[ctx.guild.id]["crpe"]['URL_s'],
                              colour=discord.Colour.from_rgb(re.randrange(0, 255), 0, re.randrange(0, 255)))
        embed.set_author(name='VASABI', url='https://github.com/VASABIcz/Simple-discord-music-bot',
                         icon_url='https://i.ytimg.com/vi_webp/xeA7VQE_R1k/maxresdefault.webp')
        embed.set_thumbnail(url=loljs[ctx.guild.id]["crpe"]['thumb'])
        # embed.add_field(name='lenght', value='10:24', inline=True)
        embed.add_field(name='status', value='playing', inline=False)
        embed.add_field(name='commands', value='_', inline=False)
        #embed.add_field(name='⏸️/▶️', value='**`pause/resume`**', inline=True)
        embed.add_field(name='❗️', value='**`disconnect`**', inline=True)
        embed.add_field(name='⏩', value='**`skip`**', inline=True)  # **`aaaaaaa`**
        message = await ctx.send(embed=embed)
        #await message.add_reaction('⏸️')
        #await message.add_reaction('▶️')
        await message.add_reaction('❗')
        await message.add_reaction('⏩')
        await asyncio.sleep(1)
        loljs[ctx.guild.id]['rpm']['mid'] = message.id
        loljs[ctx.guild.id]['rpm']['chid'] = ctx.channel.id
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
                       'ignoreerrors': True,
                       'logtostderr': False,
                       'quiet': True,
                       'no_warnings': False,
                       'default_search': 'auto',
                       'source_address': '0.0.0.0'}

        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                          'options': '-vn'}
        # ==========================================================================================================================
        # ==========================================================================================================================

        if ctx.author.voice is None:
            await ctx.send("Ur not connected to voice channel")
        else:

            ###INIT YTDL
            with YoutubeDL(YDL_OPTIONS) as ydl:

                ###HANDLE PLAYLIST/VIDEOS
                if urlee != "":
                    try:
                        info = ydl.extract_info(urlee, download=False)
                        if 'entries' in info and info['entries'] == []:
                            await ctx.send("BAD")
                        else:
                            if 'youtube.com/playlist?list=' in urlee:
                                for i in range(len(info['entries'])):
                                    loljs[ctx.guild.id]['que'].append({})
                                    thumb = loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1]['thumb'] = \
                                        info['entries'][i]['thumbnail']
                                    loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1]['URL'] = \
                                        info['entries'][i]['url']
                                    URL_s = loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1]['URL_s'] = \
                                        info['entries'][i]['webpage_url']
                                    tit = loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1]['tit'] = \
                                        info['entries'][i]['title']
                                    print(i)
                                await ctx.send('playlist is loaded')
                            else:
                                if 'entries' not in info:
                                    loljs[ctx.guild.id]['que'].append({})
                                    thumb = loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1]['thumb'] = \
                                    info[
                                        'thumbnail']
                                    loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1]['URL'] = info['url']
                                    URL_s = loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1]['URL_s'] = \
                                    info[
                                        'webpage_url']
                                    tit = loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1]['tit'] = info[
                                        'title']
                                else:
                                    loljs[ctx.guild.id]['que'].append({})
                                    thumb = loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1]['thumb'] = \
                                        info['entries'][0]['thumbnail']
                                    loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1]['URL'] = \
                                        info['entries'][0]['url']
                                    URL_s = loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1]['URL_s'] = \
                                        info['entries'][0]['webpage_url']
                                    tit = loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1]['tit'] = \
                                        info['entries'][0]['title']

                            ###CONNECT
                            if not is_connected(ctx):
                                channel = ctx.author.voice.channel
                                await channel.connect()

                            ###SEND EMBED
                            embed = discord.Embed(title=tit, url=URL_s, description='Added to que:',
                                                  colour=discord.Colour.from_rgb(re.randrange(0, 255), 0,
                                                                                 re.randrange(0, 255)))
                            embed.set_author(name='VASABI', url='https://github.com/VASABIcz/Simple-discord-music-bot',
                                             icon_url='https://i.ytimg.com/vi_webp/xeA7VQE_R1k/maxresdefault.webp')
                            embed.set_thumbnail(url=thumb)
                            if loljs[ctx.guild.id]["crpe"]['tit']:
                                embed.set_footer(text="Position in que: {}".format(len(loljs[ctx.guild.id]['que'])))
                            else:
                                if loljs[ctx.guild.id]['loop']:
                                    embed.set_footer(
                                        text="Position in que: {}".format(len(loljs[ctx.guild.id]['que'])))
                                else:
                                    embed.set_footer(text="Now playing")
                            await ctx.send(embed=embed)



                    except:
                        pass
                else:
                    if not is_connected(ctx):
                        channel = ctx.author.voice.channel
                        await channel.connect()

                    ###SOME LOOP AND INIT STUFF
                while True:
                    voice = get(bot.voice_clients, guild=ctx.guild)
                    if not voice.is_playing():
                        if is_connected(ctx):
                            if loljs[ctx.guild.id]['voice_id'] != voice.channel.id:

                                ###RESTORE PLAYED SONG WHILE MOVING BOT
                                if loljs[ctx.guild.id]["crpe"]['URL_s'] is not None:
                                    loljs[ctx.guild.id]['que'].insert(0, {})
                                    loljs[ctx.guild.id]['que'][0]['URL'] = loljs[ctx.guild.id]["crpe"]['URL']
                                    loljs[ctx.guild.id]['que'][0]['URL_s'] = loljs[ctx.guild.id]["crpe"][
                                        'URL_s']
                                    loljs[ctx.guild.id]['que'][0]['thumb'] = loljs[ctx.guild.id]["crpe"][
                                        'thumb']
                                    loljs[ctx.guild.id]['que'][0]['tit'] = loljs[ctx.guild.id]["crpe"]['tit']
                            loljs[ctx.guild.id]['voice_id'] = voice.channel.id
                            if loljs[ctx.guild.id]['que'] != []:

                                ###LOOP
                                loop = loljs[ctx.guild.id]['loop']
                                if loop:
                                    if urlee == '':
                                        urlee = None
                                    else:
                                        lenght = len(loljs[ctx.guild.id]['que'])
                                        loljs[ctx.guild.id]["crp"] += 1
                                        if loljs[ctx.guild.id]["crp"] == lenght:
                                            loljs[ctx.guild.id]["crp"] = 0

                                ###EXTRACT FROM JSON
                                URL = loljs[ctx.guild.id]['que'][loljs[ctx.guild.id]["crp"]]['URL']

                                ###STREAM AUDIO
                                try:
                                    voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                                except:
                                    await asyncio.sleep(0.1)
                                    voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                                voice.source = discord.PCMVolumeTransformer(voice.source)
                                voice.source.volume = 0.01
                                voice.is_playing()

                                ###SET CRP SONG
                                thumb = loljs[ctx.guild.id]['que'][loljs[ctx.guild.id]["crp"]]['thumb']
                                URL_s = loljs[ctx.guild.id]['que'][loljs[ctx.guild.id]["crp"]]['URL_s']
                                tit = loljs[ctx.guild.id]['que'][loljs[ctx.guild.id]["crp"]]['tit']
                                loljs[ctx.guild.id]["crpe"]['tit'] = tit
                                loljs[ctx.guild.id]["crpe"]['URL_s'] = URL_s
                                loljs[ctx.guild.id]["crpe"]['thumb'] = thumb
                                loljs[ctx.guild.id]["crpe"]['URL'] = URL

                                ###UPDATE CRP COMMAND
                                if loljs[ctx.guild.id]["crpe"]['tit'] is not None:
                                    try:
                                        embed = discord.Embed(title=loljs[ctx.guild.id]["crpe"]['tit'],
                                                              url=loljs[ctx.guild.id]["crpe"]['URL_s'], colour=discord.Colour.from_rgb(re.randrange(0, 255), 0, re.randrange(0, 255)))
                                        embed.set_author(name='VASABI',
                                                         url='https://github.com/VASABIcz/Simple-discord-music-bot',
                                                         icon_url='https://i.ytimg.com/vi_webp/xeA7VQE_R1k/maxresdefault.webp')
                                        embed.set_thumbnail(url=loljs[ctx.guild.id]["crpe"]['thumb'])
                                        # embed.add_field(name='lenght', value='10:24', inline=True)
                                        embed.add_field(name='status', value='playing', inline=False)
                                        embed.add_field(name='commands', value='_', inline=False)
                                        #embed.add_field(name='⏸️/▶️', value='**`pause/resume`**', inline=True)
                                        embed.add_field(name='❗️', value='**`disconnect`**', inline=True)
                                        embed.add_field(name='⏩', value='**`skip`**', inline=True)  # **`aaaaaaa`**
                                        chal = bot.get_channel(int(loljs[ctx.guild.id]['rpm']['chid']))
                                        message = await chal.fetch_message(loljs[ctx.guild.id]['rpm']['mid'])
                                        await message.edit(embed=embed)
                                    except:
                                        pass
                                else:
                                    pass
                                ###HANDLE LOOP
                                loop = loljs[ctx.guild.id]['loop']
                                if not loop:
                                    del loljs[ctx.guild.id]['que'][0]

                                ###SOME BULLSHIT THAT MAKES IT WORK THIS MIGHT BE BETTER
                            else:
                                loljs[ctx.guild.id]["crpe"]['tit'] = None
                                loljs[ctx.guild.id]["crpe"]['URL_s'] = None
                                loljs[ctx.guild.id]["crpe"]['thumb'] = None
                                await asyncio.sleep(0.1)
                        else:
                            await asyncio.sleep(0.1)
                    else:
                        await asyncio.sleep(0.1)

                        ###VALIDATE ALL LINKS WHILE PLAYING ANOTHER SONG TO BYPASS USER WAITING FOR VALIDATION
                        if loljs[ctx.guild.id]['que']:
                            for n in range(len(loljs[ctx.guild.id]['que'])):
                                if scrap(loljs[ctx.guild.id]['que'][n]['URL']):
                                    print('hmm')
                                    info = ydl.extract_info(loljs[ctx.guild.id]['que'][n]['URL_s'], download=False)
                                    loljs[ctx.guild.id]['que'][n]['URL'] = info['url']

###INTERACRIVE CONTROL HANDELING
@bot.event
async def on_raw_reaction_add(payload):
    global loljs

    ###handle reaction
    gid = payload.guild_id
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    user = bot.get_user(payload.user_id)
    ###HANDLED CRP COMMAND
    if loljs[gid]['rpm']['mid'] is not None:
        if payload.message_id == loljs[gid]['rpm']['mid']:
            if payload.emoji.id is not None:
                emoji = bot.get_emoji(payload.emoji.id)
            else:
                emoji = payload.emoji.name
            await message.remove_reaction(emoji, user)
            if payload.emoji.name == '⏸️':
                pass
            if payload.emoji.name == '▶️':
                pass
            if payload.emoji.name == '❗':
                guild = bot.get_guild(gid)
                voice = get(bot.voice_clients, guild=guild)
                loljs[gid]['que'] = []
                loljs[gid]['crp'] = 0
                if voice:
                    if voice.is_playing():
                        voice.stop()
            if payload.emoji.name == '⏩':
                guild = bot.get_guild(gid)
                voice = get(bot.voice_clients, guild=guild)
                if voice is not None:
                    voice.stop()

    ###HANDLE QUE COMMAND
    if loljs[gid]['quem']['mid'] is not None:
        if payload.message_id == loljs[gid]['quem']['mid']:
            if payload.emoji.id is not None:
                emoji = bot.get_emoji(payload.emoji.id)
            else:
                emoji = payload.emoji.name
            await message.remove_reaction(emoji, user)
            if payload.emoji.name == '▶️':
                loljs[gid]['quem']['pg'] += 1
            if payload.emoji.name == '◀️':
                if loljs[gid]['quem']['pg'] > 1:
                    loljs[gid]['quem']['pg'] += -1
            if payload.emoji.name == '🔄':
                pass


            nam = loljs[gid]['quem']['pg']
            qee = loljs[gid]['que']
            embed = discord.Embed(title="QUE (:", description="Song que",
                                  colour=discord.Colour.from_rgb(re.randrange(0, 255), 0, re.randrange(0, 255)))
            embed.set_author(name='VASABI', url='https://github.com/VASABIcz/Simple-discord-music-bot',
                             icon_url='https://i.ytimg.com/vi_webp/xeA7VQE_R1k/maxresdefault.webp')
            for i in range(5):
                try:
                    embed.add_field(name=qee[int(i + (nam * 5) - 5)]['tit'], value=str(i + 1 + (nam * 5) - 5),
                                    inline=False)
                except:
                    pass

            embed.set_footer(text="page<{}>".format(nam))
            chal = bot.get_channel(int(loljs[gid]['quem']['chid']))
            message = await chal.fetch_message(loljs[gid]['quem']['mid'])
            await message.edit(embed=embed)







@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('---------------------')
    activity = discord.Game(name=".help")
    await bot.change_presence(status=discord.Status.online, activity=activity)


bot.run('Njk1MjY5OTE3NjcwMjQ0Mzk0.XoXukQ.LW6f-mojf64U_QzhCzXAZIkuIHQ')
