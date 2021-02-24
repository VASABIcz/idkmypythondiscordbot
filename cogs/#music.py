import discord
from discord.ext import commands#, tasks
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
import json
import asyncio
import random as re
#import time
from constant import *

class music(commands.Cog):
    plej = True
    global loljs
    global YDL_OPTIONS
    global FFMPEG_OPTIONS
    global init
    global is_connected
    global scrap
    global validate
    global embed_crp
    global embed_que
    global embed_ns
    def __init__(self, bot):
        self.bot = bot
        self.init = init
        self.scrap = scrap
        self.validate = validate
        self.is_connected = is_connected
        self.embed_crp = embed_crp
        self.embed_que = embed_que
        self.embed_ns = embed_ns

    # PRESKOCENI PRAVE HRAJICIHO SONGU
    @commands.command(brief="skips a song", aliases=['sk', 's'])
    async def skip(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice is not None:
            voice.stop()
            await ctx.send("song has been skiped (:")
        else:
            await ctx.send("nothing to skip (((((((((:")


    @commands.command(brief="random song", aliases=['shuf'])
    async def shuffle(self, ctx):
        await init(ctx.guild.id)

        loljs[ctx.guild.id]['shuffle'] = True
        await ctx.send("shuffled")

    @commands.command(brief="unrandom song", aliases=['deshuf'])
    async def deshuffle(self, ctx):
        await init(ctx.guild.id)

        loljs[ctx.guild.id]['shuffle'] = False
        await ctx.send("deshuffled")

    ###ZASMICKOVANI RADY SONGU
    @commands.command(brief="loop a song", aliases=['lq', 'loop', 'loopqueue'])
    async def loopq(self, ctx):
        await init(ctx.guild.id)

        loljs[ctx.guild.id]['loop'] = True
        await ctx.send("que has been looped (:")

    ###ODSMICKOVANI RADY SONGU
    @commands.command(brief="stops loop a song", aliases=['ld', 'lqd', 'unloop', 'loopd'])
    async def loopqd(self, ctx):
        await self.init(ctx.guild.id)

        loljs[ctx.guild.id]['loop'] = False
        await ctx.send("que has been un looped (:")

    ###COMMAND PRO VICISTENI SONGU
    @commands.command(brief="stops all music", aliases=['del', 'clear', 'stop'])
    async def oof(self, ctx):
        await self.init(ctx.guild.id)

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
        if await self.is_connected(ctx):
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
        global loljs
        try:

            await self.init(ctx.guild.id)
            try:
                if loljs[ctx.guild.id]['quem']['chid'] is not None:
                    chal = self.bot.get_channel(loljs[ctx.guild.id]['quem']['chid'])
                    message = await chal.fetch_message(loljs[ctx.guild.id]['quem']['mid'])
                    await message.delete()
            except:
                pass
            if nam < 1:
                nam = 1
            message = await ctx.send(embed=await self.embed_que(ctx.guild.id, nam))
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
        await self.init(ctx.guild.id)
        try:
            ide = int(ide)
            if ide >= 0:
                if ide == 0:
                    if loljs[ctx.guild.id]['loop']:
                        await ctx.send(f"{loljs[ctx.guild.id]['que'][int(ide)]['tit']} has been removed from que")
                        del loljs[ctx.guild.id]['que'][int(ide)]
                    else:
                        await ctx.channel.send('BAD D:')
                else:
                    await ctx.send(f"{loljs[ctx.guild.id]['que'][int(ide)]['tit']} has been removed from que")
                    del loljs[ctx.guild.id]['que'][int(ide)]
            else:
                await ctx.channel.send("U can't remove crp D: use skip")
        except:
            await ctx.channel.send('BAD D:')

    @commands.command(brief="plays and updates song in cache", help="song name or URL", aliases=['forceplay', 'forcep'])
    async def fp(self, ctx, *, urlee=None):
        await ctx.invoke(self.bot.get_command('p'), urlee=urlee, fp=True)

    @commands.command(brief="Plays a video or playlist from a link", help="song name or URL",
                 aliases=['np', 'nowplaying', 'playing'])
    async def crp(self, ctx):
        await self.init(ctx.guild.id)
        if loljs[ctx.guild.id]["crpe"]['tit'] is not None:
            try:
                if loljs[ctx.guild.id]['rpm']['chid'] is not None:
                    chal = self.bot.get_channel(loljs[ctx.guild.id]['rpm']['chid'])
                    message = await chal.fetch_message(loljs[ctx.guild.id]['rpm']['mid'])
                    await message.delete()
            except:
                pass
            message = await ctx.send(embed=await self.embed_crp(ctx.guild.id, 'playing'))
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
        await self.init(ctx.guild.id)
        if urlee is None:
            await ctx.send(" U need to give a song name or URL (:")
            return

        if ctx.author.voice is None:
            await ctx.send("Ur not connected to voice channel")
            return

        ###LIBRARY PREZ KTEROU SE EXTRAHUJI INFORMACE O VIDEU
        ydl = YoutubeDL(YDL_OPTIONS)

        # NACTE CACHE PRO SONGY
        f = open('cache.json', 'r+')
        cache = json.load(f)


        # ZKONTOLUJE POKUD JE VIDEO V CACHE, POKUD NE EXTRAHUJE INFORMACE A PRIDA HO PRO SNIZENI ODEZVY BOTA
        if not urlee in cache or fp is True:
            ### I FUCKING DONT KNOW HOW THIS WORKS BUT IT DOES (: yoinked it from ofic bot
            # bruh just 2 random lines and it's async
            if 'youtube.com/playlist?list=' in urlee:
                await ctx.send('fetching playlist')
            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(None,
                                              lambda: ydl.extract_info(urlee, download=False))
            # print(info)
            if 'entries' in info and info['entries'] == []:
                await ctx.send("BAD")
            else:
                if 'entries' in info:
                    print('cs')
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
                    loljs[ctx.guild.id]['que'].append({})
                    thumb = loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1][
                        'thumb'] = info['thumbnail']
                    URL = loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1][
                        'URL'] = info['url']
                    URL_s = loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1][
                        'URL_s'] = info['webpage_url']
                    tit = loljs[ctx.guild.id]['que'][len(loljs[ctx.guild.id]['que']) - 1][
                        'tit'] = info['title']
                    cache[urlee] = []
                    cache[urlee].append({})
                    cache[urlee][len(cache[urlee]) - 1]['URL'] = URL
                    cache[urlee][len(cache[urlee]) - 1]['tit'] = tit
                    cache[urlee][len(cache[urlee]) - 1]['thumb'] = thumb
                    cache[urlee][len(cache[urlee]) - 1]['URL_s'] = URL_s
                with open('cache.json', 'w') as fe:
                    json.dump(cache, fe)

        else:
            for l in range(len(cache[urlee])):
                if l == 0:
                    if await self.scrap(cache[urlee][0]['URL']):
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

        ###SEND EMBED
        ###POSLE SONG KTERY SE PRDAL DO PORAD
        try:
            await self.embed_ns(ctx, tit, URL_s, thumb)
        except:
            pass

        ###SOME LOOPawait self.init STUFF
        if not await self.is_connected(ctx):
            channel = ctx.author.voice.channel.id
            chl = await self.bot.fetch_channel(channel)
            await chl.connect()


        if not loljs[ctx.guild.id]['playing']:
            loljs[ctx.guild.id]['playing'] = True

            x = asyncio.Event()

            def skipe(error=None):
                x.set()

            while True:
                voice = get(self.bot.voice_clients, guild=ctx.guild)
                if voice is not None and not voice.is_paused() and not voice.is_playing() and await self.is_connected(
                        ctx) and loljs[ctx.guild.id]['que']:
                    print('lool')
                    x.clear()
                    fid = loljs[ctx.guild.id]
                    ###LOOP
                    ###SPRAVOVANI PRAVE HRANEHO SONGU
                    loop = fid['loop']
                    if loop:
                        if fid["crpe"]['tit'] is not None:
                            if fid['shuffle']:
                                fid["crp"] += re.randint(0, len(fid['que']))
                            else:
                                fid["crp"] += 1
                            if fid["crp"] >= len(fid['que']):
                                fid["crp"] = 0
                    else:
                        if fid["crpe"]['tit'] is not None:
                            del fid['que'][fid["crp"]]
                            if fid["crp"] == len(fid['que']):
                                fid["crp"] = 0
                    if loljs[ctx.guild.id]['que']:
                        ###STREAM AUDIO
                        ###COD KTERY STREAMUJE VIDEO Z LINKU
                        URL = fid['que'][fid["crp"]]['URL']
                        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=skipe)
                        voice.source = discord.PCMVolumeTransformer(voice.source)
                        voice.source.volume = 0.05
                        fid["crpe"]['URL'] = URL
                        fid["crpe"]['thumb'] = fid['que'][fid["crp"]]['thumb']
                        fid["crpe"]['URL_s'] = fid['que'][fid["crp"]]['URL_s']
                        fid["crpe"]['tit'] = fid['que'][fid["crp"]]['tit']

                        ###UPDATE CRP COMMAND
                        ###UPDATNE CRP ZPRAVU S PRAVE HRAJICIM SONGEM
                        chid = fid['rpm']['chid']
                        if chid is not None:
                            chal = self.bot.get_channel(chid)
                            message = await chal.fetch_message(fid['rpm']['mid'])
                            await message.edit(embed=await self.embed_crp(ctx.guild.id, 'playing'))
                        else:
                            await self.validate(ctx, YDL_OPTIONS)
                    if not loljs[ctx.guild.id]['que']:
                        print('wtfee')
                        loljs[ctx.guild.id]["crpe"]['tit'] = None
                        loljs[ctx.guild.id]["crpe"]['URL_s'] = None
                        loljs[ctx.guild.id]["crpe"]['thumb'] = None
                        loljs[ctx.guild.id]["crpe"]['URL'] = None
                        loljs[ctx.guild.id]['playing'] = False
                        break
                elif not loljs[ctx.guild.id]['que']:
                    print('wtf')
                    loljs[ctx.guild.id]["crpe"]['tit'] = None
                    loljs[ctx.guild.id]["crpe"]['URL_s'] = None
                    loljs[ctx.guild.id]["crpe"]['thumb'] = None
                    loljs[ctx.guild.id]["crpe"]['URL'] = None

                    await self.validate(ctx, YDL_OPTIONS)
                    loljs[ctx.guild.id]['playing'] = False
                    break
                else:
                    print('xd')
                    await self.validate(ctx, YDL_OPTIONS)
                await asyncio.sleep(0)
                await x.wait()



def setup(bot):
    bot.add_cog(music(bot))