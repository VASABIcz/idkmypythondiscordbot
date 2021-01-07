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
###VECI KTERE JESTE BUDU DELAT NEBO JSEM DODELAL
# TODO new HELP command
# TODO while moving bot que is None VALVE PLS FIX
# DONE
# TODO interactive command que
# DONE
# TODO fix connect command
# DONE
# TODO on_voice_state_update
# testing in progres
# TODO BETER LINK VALIDATING/ CACHING
# DONE
# TODO volume controll command
#
# TODO LEPSI LOOP SPRAVOVANI
#
# TODO OBECNE ZRYCHLENI BOTA
#
# TODO ODSTRANENI ERRORU PRI POSOUVANI BOTA MEZI CHANNELY(ciste esteticke)
#
# TODO FIXOVANI MENSICH BUGU

###PRIDANI SERVRU DO DICTIONARY
def init(ctx):
    global loljs
    try:
        if ctx.guild.id not in loljs:
            loljs[ctx.guild.id] = {}
            loljs[ctx.guild.id]['loop'] = False
            loljs[ctx.guild.id]['que'] = []
            loljs[ctx.guild.id]["crp"] = 0
            loljs[ctx.guild.id]["crpe"] = {}
            loljs[ctx.guild.id]["crpe"]['tit'] = None
            loljs[ctx.guild.id]["crpe"]['URL_s'] = None
            loljs[ctx.guild.id]["crpe"]['thumb'] = None
            loljs[ctx.guild.id]["crpe"]['URL'] = None
            loljs[ctx.guild.id]['rpm'] = {}
            loljs[ctx.guild.id]['rpm']['mid'] = None
            loljs[ctx.guild.id]['rpm']['chid'] = None
            loljs[ctx.guild.id]['quem'] = {}
            loljs[ctx.guild.id]['quem']['mid'] = None
            loljs[ctx.guild.id]['quem']['chid'] = None
            loljs[ctx.guild.id]['quem']['pg'] = None

    except:
        if ctx not in loljs:
            loljs[ctx] = {}
            loljs[ctx]['loop'] = False
            loljs[ctx]['que'] = []
            loljs[ctx]["crp"] = 0
            loljs[ctx]["crpe"] = {}
            loljs[ctx]["crpe"]['tit'] = None
            loljs[ctx]["crpe"]['URL_s'] = None
            loljs[ctx]["crpe"]['thumb'] = None
            loljs[ctx]["crpe"]['URL'] = None
            loljs[ctx]['rpm'] = {}
            loljs[ctx]['rpm']['mid'] = None
            loljs[ctx]['rpm']['chid'] = None
            loljs[ctx]['quem'] = {}
            loljs[ctx]['quem']['mid'] = None
            loljs[ctx]['quem']['chid'] = None
            loljs[ctx]['quem']['pg'] = None


def is_connected(ctx):
    voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()

#EXTRAHOVANI FUCKNCNI DOBU SONGU
def scrap(URL):
    try:
        x = URL.find('expire=')
        x += 7
        y = URL.find('&ei')
        ur = int(URL[x:y])
        ur += -6000
        tim = int(time.time())
        if ur <= tim:
            return True
        else:
            return False
    except:
        x = URL.find('expire/')
        x += 7
        y = URL.find('/ei/')
        ur = int(URL[x:y])
        ur += -6000
        tim = int(time.time())
        if ur <= tim:
            return True
        else:
            return False


###COMAND PRO KONTROLU FUNKCNOSTI LINKU
def validate(ctx, YDL_OPTIONS):
    ydl = YoutubeDL(YDL_OPTIONS)
    ###VALIDATE ALL LINKS WHILE PLAYING ANOTHER SONG TO BYPASS USER WAITING FOR VALIDATION

    #VALIDATE CURRENT QUE
    if loljs[ctx.guild.id]['que']:
        for n in range(len(loljs[ctx.guild.id]['que'])):
            if scrap(loljs[ctx.guild.id]['que'][n]['URL']):
                info = ydl.extract_info(loljs[ctx.guild.id]['que'][n]['URL_s'],
                                        download=False)
                loljs[ctx.guild.id]['que'][n]['URL'] = info['url']
                print('validated que')

    #VALIDATE SAVE
    with open('save.json', 'r+') as f:
        filee = json.load(f)
        if filee != {}:
            if filee[str(ctx.author.id)]['que']:
                try:
                    for n in range(len(filee[str(ctx.author.id)]['que'])):
                        if scrap(filee[str(ctx.author.id)]['que'][n]['URL']):
                            info = ydl.extract_info(
                                filee[str(ctx.author.id)]['que'][n]['URL_s'],
                                download=False)
                            filee[str(ctx.author.id)]['que'][n]['URL'] = info['url']
                            with open('save.json', 'w') as fe:
                                json.dump(filee, fe)
                            print('validated save')
                except:
                    pass
    #VALIDATE CACHE
    with open('cache.json', 'r+') as f:
        filee = json.load(f)
        if filee != {}:
            for n in range(len(filee)):
                lil = list(filee)
                if scrap(filee[lil[n]]['URL']):
                    info = ydl.extract_info(filee[lil[n]]['URL_s'],download=False)
                    filee[lil[n]]['URL'] = info['url']
                    with open('cache.json', 'w') as fe:
                        json.dump(filee, fe)
                    print('validated cache {}'.format(lil[n]))

#PRESKOCENI PRAVE HRAJICIHO SONGU
@bot.command(brief="skips a song")
async def skip(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice is not None:
        voice.stop()
        await ctx.send("song has been skiped (:")
    else:
        await ctx.send("nothing to skip (((((((((:")

###ZASMICKOVANI RADY SONGU
@bot.command(brief="loop a song")
async def loopq(ctx):
    global loljs
    init(ctx)

    loljs[ctx.guild.id]['loop'] = True
    await ctx.send("que has been looped (:")

###ODSMICKOVANI RADY SONGU
@bot.command(brief="stops loop a song")
async def loopqd(ctx):
    global loljs
    init(ctx)

    loljs[ctx.guild.id]['loop'] = False
    await ctx.send("que has been un looped (:")

###COMMAND PRO VICISTENI SONGU
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

#KOMAND NA PINGNUTI BOTA
@bot.command(brief="test command/ping command")
async def hello(ctx):
    await ctx.channel.send("hello")

#PRIPOJI NEBO PREPOJI BOTA
@bot.command(brief="...")
async def connect(ctx):
    channel = ctx.author.voice.channel
    if is_connected(ctx):
        server = ctx.message.guild.voice_client
        await server.disconnect()
        await channel.connect()
    else:
        await channel.connect()

#ODPOJI BOTA
@bot.command(brief="disconects bot from voice channel")
async def d(ctx):
    server = ctx.message.guild.voice_client
    voice = get(bot.voice_clients, guild=ctx.guild)
    voice.stop()
    await server.disconnect()
    await ctx.send("U DcD me D:")

###VIPISE SONGY V RADE
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
    embed = discord.Embed(title="QUE (:", description="Song que",
                          colour=discord.Colour.from_rgb(re.randrange(0, 255), 0, re.randrange(0, 255)))
    embed.set_author(name='VASABI', url='https://github.com/VASABIcz/Simple-discord-music-bot',
                     icon_url='https://i.ytimg.com/vi_webp/xeA7VQE_R1k/maxresdefault.webp')
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
    await asyncio.sleep(2)
    loljs[ctx.guild.id]['quem']['mid'] = message.id
    loljs[ctx.guild.id]['quem']['chid'] = ctx.channel.id
    loljs[ctx.guild.id]['quem']['pg'] = nam

###COMMAND PRO ODSTRANENI SONGU Z RADY
@bot.command(brief="remove 1 specific song from que ", help=".r number of song (use .que)")
async def r(ctx, *, ide: int):
    global loljs
    init(ctx)
    await ctx.send(
        "{} has been removed from que".format(loljs[ctx.guild.id]['que'][int(ide - 1)]['tit']))
    del loljs[ctx.guild.id]['que'][int(ide - 1)]




@bot.command(brief="shows songs in que", help="just .que LOOOOL")
async def q(ctx, nam=1):
    await ctx.invoke(bot.get_command('que'), nam=nam)


###ULOZI UZIVATELI PLAYLIST
@bot.command(brief="Plays a single video, from a youtube URL", help="song name or URL")
async def dump(ctx):
    global loljs
    init(ctx)
    ide = ctx.author.id

    try:
        with open('save.json', 'r+') as f:
            filee = json.load(f)
    except:
        with open('save.json', 'w+') as f:
            f.write('{}')
            filee = json.load(f)

    if not str(ide) in filee:
        filee[str(ide)] = {}
        filee[str(ide)]['que'] = []
    filee[str(ide)]['que'] = loljs[ctx.guild.id]['que']

    with open('save.json', 'w') as f:
        json.dump(filee, f)

###NACTE UZIVATELEM ULOZENY PLAYLIST
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
        await ctx.invoke(bot.get_command('p'), urlee='')


@bot.command(brief="Plays a single video, from a youtube URL", help="song name or URL")
async def play(ctx, *, urlee=None):
    await ctx.invoke(bot.get_command('p'), urlee=urlee)


@bot.command(brief="Plays a video or playlist from a link", help="song name or URL")
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
        embed.add_field(name='status', value='playing', inline=False)
        embed.add_field(name='commands', value='_', inline=False)
        embed.add_field(name='⏸️/▶️', value='**`pause/resume`**', inline=True)
        embed.add_field(name='❗️', value='**`disconnect`**', inline=True)
        embed.add_field(name='⏩', value='**`skip`**', inline=True)  # **`aaaaaaa`**
        message = await ctx.send(embed=embed)
        await message.add_reaction('▶️')
        await message.add_reaction('⏸️')
        await message.add_reaction('❗')
        await message.add_reaction('⏩')
        await asyncio.sleep(2)
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
        ###PRIDA SERVER DO DICTIONARY
        init(ctx)

        ###YTDL FFMPEG SETTINGS
        #NASTAVENI PRO FFMPEG/YOUTUBE_DL
        # ==========================================================================================================================
        # ==========================================================================================================================
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
            ###LIBRARY PREZ KTEROU SE EXTRAHUJI INFORMACE O VIDEU
            with YoutubeDL(YDL_OPTIONS) as ydl:
                if urlee != "":
                    #NACTE CACHE PRO SONGY
                    with open('cache.json', 'r+') as f:
                        cache = json.load(f)
                        #ZKONTOLUJE POKUD JE VIDEO V CACHE, POKUD NE EXTRAHUJE INFORMACE A PRIDA HO PRO SNIZENI ODEZVY BOTA
                        if not urlee in cache:

                            try:
                                info = ydl.extract_info(urlee, download=False)
                                if 'entries' in info and info['entries'] == []:
                                    await ctx.send("BAD")
                                else:
                                    if 'youtube.com/playlist?list=' in urlee:
                                        for i in range(len(info['entries'])):
                                            loljs[ctx.guild.id]['que'].append({})
                                            thumb = loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1][
                                                'thumb'] = \
                                                info['entries'][i]['thumbnail']
                                            URL = loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1]['URL'] = \
                                                info['entries'][i]['url']
                                            URL_s = loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1][
                                                'URL_s'] = \
                                                info['entries'][i]['webpage_url']
                                            tit = loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1][
                                                'tit'] = \
                                                info['entries'][i]['title']
                                            print(i)
                                        await ctx.send('playlist is loaded')
                                    else:
                                        if 'entries' not in info:
                                            loljs[ctx.guild.id]['que'].append({})
                                            thumb = loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1][
                                                'thumb'] = \
                                                info['thumbnail']
                                            URL = loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1]['URL'] = \
                                            info['url']
                                            URL_s = loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1][
                                                'URL_s'] = \
                                                info[
                                                    'webpage_url']
                                            tit = loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1][
                                                'tit'] = info[
                                                'title']
                                        else:
                                            loljs[ctx.guild.id]['que'].append({})
                                            thumb = loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1][
                                                'thumb'] = \
                                                info['entries'][0]['thumbnail']
                                            URL = loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1][
                                                'URL'] = \
                                                info['entries'][0]['url']
                                            URL_s = loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1][
                                                'URL_s'] = \
                                                info['entries'][0]['webpage_url']
                                            tit = loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1][
                                                'tit'] = \
                                                info['entries'][0]['title']
                                    cache[urlee] = {}
                                    cache[urlee]['URL'] = URL
                                    cache[urlee]['tit'] = tit
                                    cache[urlee]['thumb'] = thumb
                                    cache[urlee]['URL_s'] = URL_s
                                    with open('cache.json', 'w') as fe:
                                        json.dump(cache, fe)

                                    ###CONNECT
                                    if not is_connected(ctx):
                                        channel = ctx.author.voice.channel
                                        await channel.connect()

                                    ###SEND EMBED
                                    embed = discord.Embed(title=tit, url=URL_s, description='Added to que:',colour=discord.Colour.from_rgb(re.randrange(0, 255), 0,re.randrange(0, 255)))
                                    embed.set_author(name='VASABI',url='https://github.com/VASABIcz/Simple-discord-music-bot',icon_url='https://i.ytimg.com/vi_webp/xeA7VQE_R1k/maxresdefault.webp')
                                    embed.set_thumbnail(url=thumb)
                                    if loljs[ctx.guild.id]["crpe"]['tit']:
                                        embed.set_footer(text="Position in que: {}".format(len(loljs[ctx.guild.id]['que'])))
                                    else:
                                        if loljs[ctx.guild.id]['loop']:
                                            embed.set_footer(text="Position in que: {}".format(len(loljs[ctx.guild.id]['que'])))
                                        else:
                                            embed.set_footer(text="Now playing")
                                    await ctx.send(embed=embed)

                            except:
                                pass

                        else:
                            URL = cache[urlee]['URL']
                            tit = cache[urlee]['tit']
                            thumb = cache[urlee]['thumb']
                            URL_s = cache[urlee]['URL_s']
                            if scrap(URL):
                                info = ydl.extract_info(URL_s, download=False)
                                URL = info['url']
                            loljs[ctx.guild.id]['que'].append({})
                            loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1]['thumb'] = thumb
                            loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1]['URL'] = URL
                            loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1]['URL_s'] = URL_s
                            loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1]['tit'] = tit

                            ###CONNECT
                            ###PRIPOJI BOTA POKUD NENI PRIPOJEN
                            if not is_connected(ctx):
                                channel = ctx.author.voice.channel
                                await channel.connect()

                            ###SEND EMBED
                            ###POSLE SONG KTERY SE PRDAL DO PORADI
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
                                    embed.set_footer(text="Position in que: {}".format(len(loljs[ctx.guild.id]['que'])))
                                else:
                                    embed.set_footer(text="Now playing")
                            await ctx.send(embed=embed)



                else:
                    if not is_connected(ctx):
                        channel = ctx.author.voice.channel
                        await channel.connect()

                    ###SOME LOOP AND INIT STUFF
                while True:
                    voice = get(bot.voice_clients, guild=ctx.guild)
                    if voice is not None:
                        if not voice.is_paused():
                            if not voice.is_playing():
                                if is_connected(ctx):
                                    loljs[ctx.guild.id]['voice_id'] = voice.channel.id
                                    if loljs[ctx.guild.id]['que']:

                                        ###LOOP
                                        ###SPRAVOVANI PRAVE HRANEHO SONGU
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
                                        #EXTRAKCE POTREBNYCH VECI Z DICTIONARY/JSONU
                                        URL = loljs[ctx.guild.id]['que'][loljs[ctx.guild.id]["crp"]]['URL']
                                        thumb = loljs[ctx.guild.id]['que'][loljs[ctx.guild.id]["crp"]]['thumb']
                                        URL_s = loljs[ctx.guild.id]['que'][loljs[ctx.guild.id]["crp"]]['URL_s']
                                        tit = loljs[ctx.guild.id]['que'][loljs[ctx.guild.id]["crp"]]['tit']
                                        ###HANDLE LOOP
                                        loop = loljs[ctx.guild.id]['loop']
                                        if not loop:
                                            del loljs[ctx.guild.id]['que'][0]

                                        ###STREAM AUDIO
                                        ###COD KTERY STREAMUJE VIDEO Z LINKU
                                        try:
                                            voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                                        except:
                                            await asyncio.sleep(0.5)
                                            voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                                        voice.source = discord.PCMVolumeTransformer(voice.source)
                                        voice.source.volume = 0.01
                                        voice.is_playing()

                                        ###SET CRP SONG
                                        ###NASTAVI PRAVE HRAJICI SONG
                                        loljs[ctx.guild.id]["crpe"]['tit'] = tit
                                        loljs[ctx.guild.id]["crpe"]['URL_s'] = URL_s
                                        loljs[ctx.guild.id]["crpe"]['thumb'] = thumb
                                        loljs[ctx.guild.id]["crpe"]['URL'] = URL


                                        ###UPDATE CRP COMMAND
                                        ###UPDATNE CRP ZPRAVU S PRAVE HRAJICIM SONGEM
                                        if loljs[ctx.guild.id]["crpe"]['tit'] is not None:
                                            try:
                                                embed = discord.Embed(title=loljs[ctx.guild.id]["crpe"]['tit'],
                                                                      url=loljs[ctx.guild.id]["crpe"]['URL_s'],
                                                                      colour=discord.Colour.from_rgb(
                                                                          re.randrange(0, 255),
                                                                          0,
                                                                          re.randrange(0, 255)))
                                                embed.set_author(name='VASABI',
                                                                 url='https://github.com/VASABIcz/Simple-discord-music-bot',
                                                                 icon_url='https://i.ytimg.com/vi_webp/xeA7VQE_R1k/maxresdefault.webp')
                                                embed.set_thumbnail(url=loljs[ctx.guild.id]["crpe"]['thumb'])
                                                # embed.add_field(name='lenght', value='10:24', inline=True)
                                                embed.add_field(name='status', value='playing', inline=False)
                                                embed.add_field(name='commands', value='_', inline=False)
                                                embed.add_field(name='⏸️/▶️', value='**`pause/resume`**', inline=True)
                                                embed.add_field(name='❗️', value='**`disconnect`**', inline=True)
                                                embed.add_field(name='⏩', value='**`skip`**',
                                                                inline=True)  # **`aaaaaaa`**
                                                chal = bot.get_channel(int(loljs[ctx.guild.id]['rpm']['chid']))
                                                message = await chal.fetch_message(loljs[ctx.guild.id]['rpm']['mid'])
                                                await message.edit(embed=embed)
                                            except:
                                                pass
                                        else:
                                            pass


                                        ###
                                    else:
                                        await asyncio.sleep(0.1)#UDRZUJE ABY SE BOT NEPREHLTIL
                                        validate(ctx, YDL_OPTIONS)#ZKONTROLUJE JESTLI JSOU LINKY K MUSIC FILU FUNKCI A UDRZUJE JE FUNKCNI
                                else:
                                    await asyncio.sleep(0.1)
                                    validate(ctx, YDL_OPTIONS)
                            else:
                                await asyncio.sleep(0.1)
                                validate(ctx, YDL_OPTIONS)
                        else:
                            await asyncio.sleep(0.1)
                            validate(ctx, YDL_OPTIONS)
                    else:
                        await asyncio.sleep(0.1)
                        validate(ctx, YDL_OPTIONS)


###INTERACRIVE CONTROL HANDELING
###INTERAKTIVNI OVLADANI PREZ REAKCE
@bot.event
async def on_raw_reaction_add(payload):
    global loljs

    ###handle reaction
    gid = payload.guild_id
    init(gid)
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    user = bot.get_user(payload.user_id)

    #HANDLED CRP COMMAND
    #OVLADANI NA CRP COMMAND (NAPISE SONG KTERY PRAVE HRAJE)
    if loljs[gid]['rpm']['mid'] is not None:
        if payload.message_id == loljs[gid]['rpm']['mid']:
            if payload.emoji.id is not None:
                emoji = bot.get_emoji(payload.emoji.id)
            else:
                emoji = payload.emoji.name
            await message.remove_reaction(emoji, user)
            if payload.emoji.name == '⏸️':
                guild = bot.get_guild(gid)
                voice = get(bot.voice_clients, guild=guild)
                voice.pause()
            if payload.emoji.name == '▶️':
                guild = bot.get_guild(gid)
                voice = get(bot.voice_clients, guild=guild)
                voice.resume()
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

    #HANDLE QUE COMMAND
    #OVLADANI PRO QUE COMMAND KTERY POSLE SONGY KTERE JSOU V PORADI
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

###POKUD NEKDO MOVNE BOTA TAK NAVRATI HRAJICI SONG
@bot.event
async def on_voice_state_update(member, before, after):
    global loljs
    if after is None:
        pass
    else:
        try:
            gid = after.channel.guild.id
            init(gid)
            if member.id == bot.user.id:
                if loljs[gid]["crpe"]['URL_s'] is not None:
                    loljs[gid]['que'].insert(0, {})
                    loljs[gid]['que'][0]['URL'] = loljs[gid]["crpe"]['URL']
                    loljs[gid]['que'][0]['URL_s'] = loljs[gid]["crpe"][
                        'URL_s']
                    loljs[gid]['que'][0]['thumb'] = loljs[gid]["crpe"][
                        'thumb']
                    loljs[gid]['que'][0]['tit'] = loljs[gid]["crpe"]['tit']
        except:
            print('I DUNO')

###NAPISE KDYZ JE BOT PRIPRAVEN K POUZIVANI
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('---------------------')
    activity = discord.Game(name=".help")
    await bot.change_presence(status=discord.Status.online, activity=activity)

###DISCORD BOT TOKEN
bot.run('Njk1MjY5OTE3NjcwMjQ0Mzk0.XoXukQ.c-g-3fDfknfZ8A2tD1PfvmNCXY0')
