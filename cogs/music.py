import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
import json
import asyncio
import random as re
import time
from constant import *

class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def init(self, ctx):
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

    def is_connected(self, ctx):
        voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
        return voice_client and voice_client.is_connected()

    # EXTRAHOVANI FUCKNCNI DOBU SONGU
    def scrap(self, URL):
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
    async def validate(self, ctx, YDL_OPTIONS):
        ydl = YoutubeDL(YDL_OPTIONS)
        ###VALIDATE ALL LINKS WHILE PLAYING ANOTHER SONG TO BYPASS USER WAITING FOR VALIDATION

        # VALIDATE CURRENT QUE
        if loljs[ctx.guild.id]['que']:
            for n in range(len(loljs[ctx.guild.id]['que'])):
                if self.scrap(loljs[ctx.guild.id]['que'][n]['URL']):
                    loop = asyncio.get_event_loop()
                    info = await loop.run_in_executor(None,
                                                      lambda: ydl.extract_info(loljs[ctx.guild.id]['que'][n]['URL_s'],
                                                                               download=False))
                    loljs[ctx.guild.id]['que'][n]['URL'] = info['url']
                    print('validated que')

        # VALIDATE SAVE
        with open('save.json', 'r+') as f:
            filee = json.load(f)
            if filee != {}:
                if str(ctx.author.id) in filee:
                    if filee[str(ctx.author.id)]['que']:
                        try:
                            for n in range(len(filee[str(ctx.author.id)]['que'])):
                                if self.scrap(filee[str(ctx.author.id)]['que'][n]['URL']):
                                    loop = asyncio.get_event_loop()
                                    info = await loop.run_in_executor(None, lambda: ydl.extract_info(
                                        filee[str(ctx.author.id)]['que'][n]['URL_s'], download=False))

                                    filee[str(ctx.author.id)]['que'][n]['URL'] = info['url']
                                    with open('save.json', 'w') as fe:
                                        json.dump(filee, fe)
                                    print('validated save')
                        except:
                            pass
        # VALIDATE CACHE
        with open('cache.json', 'r+') as f:
            filee = json.load(f)
            if filee != {}:
                for n in range(len(filee)):
                    lil = list(filee)
                    for i in range(len(filee[lil[n]])):
                        if self.scrap(filee[lil[n]][i]['URL']):
                            loop = asyncio.get_event_loop()
                            info = await loop.run_in_executor(None, lambda: ydl.extract_info(
                                filee[lil[n]][i]['URL_s'], download=False))
                            filee[lil[n]][i]['URL'] = info['url']
                            with open('cache.json', 'w') as fe:
                                json.dump(filee, fe)
                            print('validated cache {}'.format(lil[n]))


    def embed_crp(self, gid, play):
        embed = discord.Embed(title=loljs[gid]["crpe"]['tit'],
                              url=loljs[gid]["crpe"]['URL_s'],
                              colour=discord.Colour.from_rgb(
                                  re.randint(0, 255),
                                  0,
                                  re.randint(0, 255)))
        embed.set_author(name='VASABI',
                         url='https://github.com/VASABIcz/Simple-discord-music-bot',
                         icon_url='https://i.ytimg.com/vi_webp/xeA7VQE_R1k/maxresdefault.webp')
        embed.set_thumbnail(url=loljs[gid]["crpe"]['thumb'])
        embed.add_field(name='status', value=play, inline=False)
        embed.add_field(name='commands', value='_', inline=False)
        embed.add_field(name='⏸️/▶️', value='**`pause/resume`**', inline=True)
        embed.add_field(name='❗️', value='**`disconnect`**', inline=True)
        embed.add_field(name='⏩', value='**`skip`**',
                        inline=True)  # **`aaaaaaa`**
        return embed

    def embed_que(self, gid, nam):
        qee = loljs[gid]['que']
        embed = discord.Embed(title="QUE (:", description="Song que",
                              colour=discord.Colour.from_rgb(re.randint(0, 255), 0, re.randint(0, 255)))
        embed.set_author(name='VASABI', url='https://github.com/VASABIcz/Simple-discord-music-bot',
                         icon_url='https://i.ytimg.com/vi_webp/xeA7VQE_R1k/maxresdefault.webp')
        for i in range(5):
            rov = i + (nam * 5) - 5
            try:
                embed.add_field(name=qee[int(rov)]['tit'], value=str(rov), inline=False)
            except:
                pass
        embed.set_footer(text="page<{}>".format(nam))
        return embed

    async def embed_ns(self, ctx, tit, URL_s, thumb):
        embed = discord.Embed(title=tit, url=URL_s, description='Added to que:',
                              colour=discord.Colour.from_rgb(re.randint(0, 255), 0,
                                                             re.randint(0, 255)))
        embed.set_author(name='VASABI', url='https://github.com/VASABIcz/Simple-discord-music-bot',
                         icon_url='https://i.ytimg.com/vi_webp/xeA7VQE_R1k/maxresdefault.webp')
        embed.set_thumbnail(url=thumb)
        if loljs[ctx.guild.id]["crpe"]['tit']:
            embed.set_footer(text="Position in que: {}".format(len(loljs[ctx.guild.id]['que']) - 1))
        else:
            if loljs[ctx.guild.id]['loop']:
                embed.set_footer(text="Position in que: {}".format(len(loljs[ctx.guild.id]['que']) - 1))
            else:
                embed.set_footer(text="Now playing")
        await ctx.send(embed=embed)

    # PRESKOCENI PRAVE HRAJICIHO SONGU
    @commands.command(brief="skips a song", aliases=['sk', 's'])
    async def skip(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice is not None:
            voice.stop()
            await ctx.send("song has been skiped (:")
        else:
            await ctx.send("nothing to skip (((((((((:")

    ###ZASMICKOVANI RADY SONGU
    @commands.command(brief="loop a song", aliases=['lq', 'loop', 'loopqueue'])
    async def loopq(self, ctx):
        global loljs
        self.init(ctx)

        loljs[ctx.guild.id]['loop'] = True
        await ctx.send("que has been looped (:")

    ###ODSMICKOVANI RADY SONGU
    @commands.command(brief="stops loop a song", aliases=['ld', 'lqd', 'unloop', 'loopd'])
    async def loopqd(self, ctx):
        global loljs
        self.init(ctx)

        loljs[ctx.guild.id]['loop'] = False
        await ctx.send("que has been un looped (:")

    ###COMMAND PRO VICISTENI SONGU
    @commands.command(brief="stops all music", aliases=['del', 'clear'])
    async def oof(self, ctx):
        global loljs
        self.init(ctx)

        voice = get(self.bot.voice_clients, guild=ctx.guild)
        loljs[ctx.guild.id]['que'] = []
        loljs[ctx.guild.id]['crp'] = 0
        if voice:
            if voice.is_playing():
                voice.stop()
                await ctx.send("U have succesfully oofed the bot")

    # KOMAND NA PINGNUTI BOTA
    @commands.command(brief="test command/ping command")
    async def hello(self, ctx):
        await ctx.channel.send("hello")

    # PRIPOJI NEBO PREPOJI BOTA
    @commands.command(brief="...", aliases=['c', 'cn', 'join'])
    async def connect(self, ctx):
        channel = ctx.author.voice.channel
        if self.is_connected(ctx):
            server = ctx.message.guild.voice_client
            await server.disconnect()
            await channel.connect()
        else:
            await channel.connect()

    # ODPOJI BOTA
    @commands.command(brief="disconects bot from voice channel", aliases=['dc', 'disconnect'])
    async def d(self, ctx):
        server = ctx.message.guild.voice_client
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        voice.stop()
        await server.disconnect()
        await ctx.send("U DcD me D:")

    ###VIPISE SONGY V RADE
    @commands.command(brief="shows songs in que", help="just .que LOOOOL", aliases=['queue', 'q'])
    async def que(self, ctx, nam=1):
        try:
            global loljs
            self.init(ctx)
            try:
                if loljs[ctx.guild.id]['quem']['chid'] is not None:
                    chal = self.bot.get_channel(loljs[ctx.guild.id]['quem']['chid'])
                    message = await chal.fetch_message(loljs[ctx.guild.id]['quem']['mid'])
                    await message.delete()
            except:
                pass
            if nam < 1:
                nam = 1
            message = await ctx.send(embed=self.embed_que(ctx.guild.id, nam))
            await message.add_reaction('◀️')
            await message.add_reaction('▶️')
            await message.add_reaction('🔄')
            loljs[ctx.guild.id]['quem']['mid'] = message.id
            loljs[ctx.guild.id]['quem']['chid'] = ctx.channel.id
            loljs[ctx.guild.id]['quem']['pg'] = nam
        except:
            await ctx.channel.send('BAD D:')

    ###COMMAND PRO ODSTRANENI SONGU Z RADY
    @commands.command(brief="remove 1 specific song from que ", help=".r number of song (use .que)",
                 aliases=['remove', 're'])
    async def r(self, ctx, ide):
        global loljs
        self.init(ctx)
        try:
            ide = int(ide)
            if ide >= 0:
                if ide == 0:
                    if loljs[ctx.guild.id]['loop']:
                        await ctx.send(
                            "{} has been removed from que".format(loljs[ctx.guild.id]['que'][int(ide)]['tit']))
                        del loljs[ctx.guild.id]['que'][int(ide)]
                    else:
                        await ctx.channel.send('BAD D:')
                else:
                    await ctx.send(
                        "{} has been removed from que".format(loljs[ctx.guild.id]['que'][int(ide)]['tit']))
                    del loljs[ctx.guild.id]['que'][int(ide)]
            else:
                await ctx.channel.send("U can't remove crp D: use skip")
        except:
            await ctx.channel.send('BAD D:')

    ###ULOZI UZIVATELI PLAYLIST
    @commands.command(brief="Plays a single video, from a youtube URL", help="song name or URL", aliases=['dp', 'save'])
    async def dump(self, ctx):
        global loljs
        self.init(ctx)
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
    @commands.command(brief="Plays a single video, from a youtube URL", help="song name or URL", aliases=['lod'])
    async def load(self, ctx):
        global loljs
        idd = ctx.author.id

        self.init(ctx)

        try:
            with open('save.json', 'r+') as f:
                filee = json.load(f)
        except:
            with open('save.json', 'w+') as f:
                f.write('{}')
                filee = json.load(f)

        loljs[ctx.guild.id]['que'].extend(filee[str(idd)]['que'])

        if not filee[str(idd)]['que']:
            await ctx.send("U didnt save any que D:")
        else:
            if loljs[ctx.guild.id]['que']:

                ###VALIDATE FIRST LINK/
                if self.scrap(loljs[ctx.guild.id]['que'][0]['URL']):
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
                    loop = asyncio.get_event_loop()
                    info = await loop.run_in_executor(None,
                                                      lambda: ydl.extract_info(loljs[ctx.guild.id]['que'][0]['URL_s'],
                                                                               download=False))
                    loljs[ctx.guild.id]['que'][0]['URL'] = info['url']
            await ctx.invoke(self.bot.get_command('p'), urlee='')

    @commands.command(brief="plays and updates song in cache", help="song name or URL", aliases=['forceplay', 'forcep'])
    async def fp(self, ctx, *, urlee=None):
        await ctx.invoke(self.bot.get_command('p'), urlee=urlee, fp=True)

    @commands.command(brief="Plays a video or playlist from a link", help="song name or URL",
                 aliases=['np', 'nowplaying', 'playing'])
    async def crp(self, ctx):
        self.init(ctx)
        global loljs
        if loljs[ctx.guild.id]["crpe"]['tit'] is not None:
            try:
                if loljs[ctx.guild.id]['rpm']['chid'] is not None:
                    chal = self.bot.get_channel(loljs[ctx.guild.id]['rpm']['chid'])
                    message = await chal.fetch_message(loljs[ctx.guild.id]['rpm']['mid'])
                    await message.delete()
            except:
                pass
            message = await ctx.send(embed=self.embed_crp(ctx.guild.id, 'playing'))
            await message.add_reaction('▶️')
            await message.add_reaction('⏸️')
            await message.add_reaction('❗')
            await message.add_reaction('⏩')
            loljs[ctx.guild.id]['rpm']['mid'] = message.id
            loljs[ctx.guild.id]['rpm']['chid'] = ctx.channel.id
        else:
            await ctx.send("Nothing is playing")

    @commands.command(brief="Plays a single video, from a youtube URL", help="song name or URL",
                 aliases=['play', 'jamm', 'pl'])
    async def p(self, ctx, *, urlee=None, fp=None):
        if urlee is None:
            await ctx.send(" U need to give a song name or URL (:")
        else:
            global loljs

            ###INITS SERVER
            ###PRIDA SERVER DO DICTIONARY
            self.init(ctx)

            ###YTDL FFMPEG SETTINGS
            # NASTAVENI PRO FFMPEG/YOUTUBE_DL
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
                        # NACTE CACHE PRO SONGY
                        with open('cache.json', 'r+') as f:
                            cache = json.load(f)
                            # ZKONTOLUJE POKUD JE VIDEO V CACHE, POKUD NE EXTRAHUJE INFORMACE A PRIDA HO PRO SNIZENI ODEZVY BOTA
                            if not urlee in cache or fp is True:
                                try:
                                    ###CONNECT
                                    if not self.is_connected(ctx):
                                        channel = ctx.author.voice.channel.id
                                        chl = await self.bot.fetch_channel(channel)
                                        await chl.connect()

                                    ### I FUCKING DONT KNOW HOW THIS WORKS BUT IT DOES (: yoinked it from ofic bot
                                    # bruh just 2 random lines and it's async
                                    loop = asyncio.get_event_loop()
                                    info = await loop.run_in_executor(None,
                                                                      lambda: ydl.extract_info(urlee, download=False))
                                    if 'entries' in info and info['entries'] == []:
                                        await ctx.send("BAD")
                                    else:
                                        if 'youtube.com/playlist?list=' in urlee:
                                            cache[urlee] = []
                                            for i in range(len(info['entries'])):
                                                loljs[ctx.guild.id]['que'].append({})
                                                thumb = loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1][
                                                    'thumb'] = \
                                                    info['entries'][i]['thumbnail']
                                                URL = loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1][
                                                    'URL'] = \
                                                    info['entries'][i]['url']
                                                URL_s = loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1][
                                                    'URL_s'] = \
                                                    info['entries'][i]['webpage_url']
                                                tit = loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1][
                                                    'tit'] = \
                                                    info['entries'][i]['title']
                                                cache[urlee].append({})
                                                cache[urlee][len(cache[urlee]) - 1]['URL'] = URL
                                                cache[urlee][len(cache[urlee]) - 1]['tit'] = tit
                                                cache[urlee][len(cache[urlee]) - 1]['thumb'] = thumb
                                                cache[urlee][len(cache[urlee]) - 1]['URL_s'] = URL_s
                                            await ctx.send('playlist is loaded')
                                        else:
                                            if 'entries' not in info:
                                                loljs[ctx.guild.id]['que'].append({})
                                                thumb = loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1][
                                                    'thumb'] = info['thumbnail']
                                                URL = loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1][
                                                    'URL'] = info['url']
                                                URL_s = loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1][
                                                    'URL_s'] = info['webpage_url']
                                                tit = loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1][
                                                    'tit'] = info['title']
                                            else:
                                                loljs[ctx.guild.id]['que'].append({})
                                                thumb = loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1][
                                                    'thumb'] = info['entries'][0]['thumbnail']
                                                URL = loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1][
                                                    'URL'] = info['entries'][0]['url']
                                                URL_s = loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1][
                                                    'URL_s'] = info['entries'][0]['webpage_url']
                                                tit = loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1][
                                                    'tit'] = info['entries'][0]['title']
                                            cache[urlee] = []
                                            cache[urlee].append({})
                                            cache[urlee][len(cache[urlee]) - 1]['URL'] = URL
                                            cache[urlee][len(cache[urlee]) - 1]['tit'] = tit
                                            cache[urlee][len(cache[urlee]) - 1]['thumb'] = thumb
                                            cache[urlee][len(cache[urlee]) - 1]['URL_s'] = URL_s
                                        with open('cache.json', 'w') as fe:
                                            json.dump(cache, fe)
                                except:
                                    pass

                            else:
                                for l in range(len(cache[urlee])):
                                    if l == 0:
                                        if self.scrap(cache[urlee][0]['URL']):
                                            loop = asyncio.get_event_loop()
                                            info = await loop.run_in_executor(None, lambda: ydl.extract_info(
                                                cache[urlee][0]['URL_s'],
                                                download=False))
                                            cache[urlee][0]['URL'] = info['url']
                                    loljs[ctx.guild.id]['que'].append(cache[urlee][l])

                                # URL = cache[urlee][len(cache[urlee])-1]['URL']
                                tit = cache[urlee][len(cache[urlee]) - 1]['tit']
                                thumb = cache[urlee][len(cache[urlee]) - 1]['thumb']
                                URL_s = cache[urlee][len(cache[urlee]) - 1]['URL_s']

                                ###CONNECT
                                ###PRIPOJI BOTA POKUD NENI PRIPOJEN
                                if not self.is_connected(ctx):
                                    channel = ctx.author.voice.channel
                                    await channel.connect()

                            ###SEND EMBED
                            ###POSLE SONG KTERY SE PRDAL DO PORAD
                            await self.embed_ns(ctx, tit, URL_s, thumb)
                    else:
                        if not self.is_connected(ctx):
                            channel = ctx.author.voice.channel
                            await channel.connect()

                        ###SOME LOOP AND INIT STUFF
                    while True:
                        voice = get(self.bot.voice_clients, guild=ctx.guild)
                        if voice is not None:
                            if not voice.is_paused():
                                if not voice.is_playing():
                                    if self.is_connected(ctx):
                                        if loljs[ctx.guild.id]['que']:
                                            ###LOOP
                                            ###SPRAVOVANI PRAVE HRANEHO SONGU
                                            loop = loljs[ctx.guild.id]['loop']
                                            if loop:
                                                if loljs[ctx.guild.id]["crpe"]['tit'] is not None:
                                                    loljs[ctx.guild.id]["crp"] += 1
                                                    if loljs[ctx.guild.id]["crp"] >= len(loljs[ctx.guild.id]['que']):
                                                        loljs[ctx.guild.id]["crp"] = 0
                                            else:
                                                if loljs[ctx.guild.id]["crpe"]['tit'] is not None:
                                                    del loljs[ctx.guild.id]['que'][loljs[ctx.guild.id]["crp"]]
                                                    if loljs[ctx.guild.id]["crp"] == len(loljs[ctx.guild.id]['que']):
                                                        loljs[ctx.guild.id]["crp"] = 0
                                        else:
                                            loljs[ctx.guild.id]["crpe"]['tit'] = None
                                            loljs[ctx.guild.id]["crpe"]['URL_s'] = None
                                            loljs[ctx.guild.id]["crpe"]['thumb'] = None
                                            loljs[ctx.guild.id]["crpe"]['URL'] = None

                                        if loljs[ctx.guild.id]['que']:

                                            ###EXTRACT FROM JSON
                                            # EXTRAKCE POTREBNYCH VECI Z DICTIONARY/JSONU
                                            URL = loljs[ctx.guild.id]['que'][loljs[ctx.guild.id]["crp"]]['URL']
                                            thumb = loljs[ctx.guild.id]['que'][loljs[ctx.guild.id]["crp"]]['thumb']
                                            URL_s = loljs[ctx.guild.id]['que'][loljs[ctx.guild.id]["crp"]]['URL_s']
                                            tit = loljs[ctx.guild.id]['que'][loljs[ctx.guild.id]["crp"]]['tit']
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
                                                    chal = self.bot.get_channel(int(loljs[ctx.guild.id]['rpm']['chid']))
                                                    message = await chal.fetch_message(
                                                        loljs[ctx.guild.id]['rpm']['mid'])
                                                    await message.edit(embed=self.embed_crp(ctx.guild.id, 'playing'))
                                                except:
                                                    pass
                                            else:
                                                pass


                                        else:
                                            await asyncio.sleep(0.01)  # UDRZUJE ABY SE BOT NEPREHLTIL
                                            await self.validate(ctx,
                                                           YDL_OPTIONS)  # ZKONTROLUJE JESTLI JSOU LINKY K MUSIC FILU FUNKCI A UDRZUJE JE FUNKCNI
                                    else:
                                        await asyncio.sleep(0.01)
                                        await self.validate(ctx, YDL_OPTIONS)
                                else:
                                    await asyncio.sleep(0.01)
                                    await self.validate(ctx, YDL_OPTIONS)
                            else:
                                await asyncio.sleep(0.01)
                                await self.validate(ctx, YDL_OPTIONS)
                        else:
                            await asyncio.sleep(0.01)
                            await self.validate(ctx, YDL_OPTIONS)


    ###INTERACRIVE CONTROL HANDELING
    ###INTERAKTIVNI OVLADANI PREZ REAKCE
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        global loljs

        ###handle reaction
        gid = payload.guild_id
        self.init(gid)
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = await self.bot.fetch_user(payload.user_id)

        # HANDLED CRP COMMAND
        # OVLADANI NA CRP COMMAND (NAPISE SONG KTERY PRAVE HRAJE)
        if payload.user_id != self.bot.user.id:
            if loljs[gid]['rpm']['mid'] is not None:
                if payload.message_id == loljs[gid]['rpm']['mid']:
                    if payload.emoji.id is not None:
                        emoji = self.bot.get_emoji(payload.emoji.id)
                    else:
                        emoji = payload.emoji.name
                    await message.remove_reaction(emoji, user)
                    if payload.emoji.name == '⏸️':
                        guild = self.bot.get_guild(gid)
                        voice = get(self.bot.voice_clients, guild=guild)
                        voice.pause()
                        try:
                            chal = self.bot.get_channel(int(loljs[gid]['rpm']['chid']))
                            message = await chal.fetch_message(loljs[gid]['rpm']['mid'])
                            await message.edit(embed=self.embed_crp(gid, 'paused'))
                        except:
                            pass
                    if payload.emoji.name == '▶️':
                        guild = self.bot.get_guild(gid)
                        voice = get(self.bot.voice_clients, guild=guild)
                        voice.resume()
                        try:
                            chal = self.bot.get_channel(int(loljs[gid]['rpm']['chid']))
                            message = await chal.fetch_message(loljs[gid]['rpm']['mid'])
                            await message.edit(embed=self.embed_crp(gid, 'playing'))
                        except:
                            pass
                    if payload.emoji.name == '❗':
                        guild = self.bot.get_guild(gid)
                        voice = get(self.bot.voice_clients, guild=guild)
                        loljs[gid]['que'] = []
                        loljs[gid]['crp'] = 0
                        if voice:
                            if voice.is_playing():
                                voice.stop()
                            await voice.disconnect()

                    if payload.emoji.name == '⏩':
                        guild = self.bot.get_guild(gid)
                        voice = get(self.bot.voice_clients, guild=guild)
                        if voice is not None:
                            voice.stop()

            # HANDLE QUE COMMAND
            # OVLADANI PRO QUE COMMAND KTERY POSLE SONGY KTERE JSOU V PORADI
            if loljs[gid]['quem']['mid'] is not None:
                if payload.message_id == loljs[gid]['quem']['mid']:
                    if payload.emoji.id is not None:
                        emoji = self.bot.get_emoji(payload.emoji.id)
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
                    chal = self.bot.get_channel(int(loljs[gid]['quem']['chid']))
                    message = await chal.fetch_message(loljs[gid]['quem']['mid'])
                    await message.edit(embed=self.embed_que(gid, nam))




def setup(bot):
    bot.add_cog(music(bot))
