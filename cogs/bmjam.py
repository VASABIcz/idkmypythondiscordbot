import discord
from discord.ext import commands, tasks
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
import json
import asyncio
import random as re
#import time
from bconstant import *
#from discord.ext import menus

#class Yes(menus.Menu):
#   def __init__(self, gid, status):
#     super().__init__()
#       self.gid = gid
#       self.status = status
#   async def send_initial_message(self, ctx, channel):
#       f = open('bcache.json', 'r+')
#       cache = json.load(f)
#       embed = discord.Embed(title=cache[loljs[self.gid]["crpe"]]['tit'],
#                             url=cache[loljs[self.gid]["crpe"]]['URL_s'],
#                             colour=0xe91e63)
#       embed.set_author(name='VASABI',
#                        url='https://github.com/VASABIcz/Simple-discord-music-bot',
#                        icon_url='https://i.ytimg.com/vi_webp/xeA7VQE_R1k/maxresdefault.webp')
#       embed.set_thumbnail(url=cache[loljs[self.gid]["crpe"]]['thumb'])
#       embed.add_field(name='status', value=self.status, inline=False)
#       embed.add_field(name='commands', value='_', inline=False)
#       embed.add_field(name='⏸️/▶️', value='**`pause/resume`**', inline=True)
#       embed.add_field(name='❗️', value='**`disconnect`**', inline=True)
#       embed.add_field(name='⏩', value='**`skip`**', inline=True)
#       return await channel.send(embed=embed)
#
#   @menus.button('\N{Black Right-Pointing Triangle}')
#    async def on_resume(self, payload):
#       await self.message.edit(content=f'Thanks {self.ctx.author}!')
#
#    @menus.button('\N{Double Vertical Bar}')
#    async def on_pause(self, payload):
#        await self.message.edit(content=f'Thanks {self.ctx.author}!')
#
#    @menus.button('\N{Black Right-Pointing Double Triangle}')
#    async def on_skip(self, payload):
#        await self.ctx.invoke(self.bot.get_command('skip'))
#
#    @menus.button('\N{Heavy Exclamation Mark Symbol}')
#    async def on_stop(self, payload):
#        await self.ctx.invoke(self.bot.get_command('oof'))
#        self.stop()

#    async def on(self, ctx):
#        await self.start(ctx)
class music(commands.Cog):
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
    global cache
    global index
    def __init__(self, bot):
        self.bot = bot
        self.init = init
        self.scrap = scrap
        self.validate = validate
        self.is_connected = is_connected
        self.embed_crp = embed_crp
        self.embed_que = embed_que
        self.embed_ns = embed_ns
        self.vali.start()

    #@commands.command()
    #async def menu_example(self, ctx):
    #   await Yes(ctx, "playing").on(ctx)


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
    @commands.command(brief="shows songs in que", help="just que LOOOOL", aliases=['queue', 'q'])
    async def que(self, ctx, nam=1):
        f = open('bcache.json', 'r+')
        cache = json.load(f)
        global loljs
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
        message = await ctx.send(embed=await self.embed_que(ctx.guild.id, nam, cache))
        await message.add_reaction('◀️')
        await message.add_reaction('▶️')
        await message.add_reaction('🔄')
        loljs[ctx.guild.id]['quem']['mid'] = message.id
        loljs[ctx.guild.id]['quem']['chid'] = ctx.channel.id
        loljs[ctx.guild.id]['quem']['pg'] = nam
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
    @commands.command(brief="plays and updates song in cache", help="song name or URL",
                      aliases=['forceplay', 'forcep'])
    async def fp(self, ctx, *, urlee=None):
        await ctx.invoke(self.bot.get_command('p'), urlee=urlee, fp=True)
    @commands.command(brief="Plays a video or playlist from a link", help="song name or URL",
                      aliases=['np', 'nowplaying', 'playing'])
    async def crp(self, ctx):
        f = open('bcache.json', 'r+')
        cache = json.load(f)
        await self.init(ctx.guild.id)
        if loljs[ctx.guild.id]["crpe"] is not None:
            try:
                if loljs[ctx.guild.id]['rpm']['chid'] is not None:
                    chal = self.bot.get_channel(loljs[ctx.guild.id]['rpm']['chid'])
                    message = await chal.fetch_message(loljs[ctx.guild.id]['rpm']['mid'])
                    await message.delete()
            except:
                pass
            message = await ctx.send(embed=await self.embed_crp(ctx.guild.id, 'playing', cache))
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


        # ZKONTOLUJE POKUD JE VIDEO V CACHE, POKUD NE EXTRAHUJE INFORMACE A PRIDA HO PRO SNIZENI ODEZVY BOTA
        await ctx.message.add_reaction('✅')
        f = open('bcache.json', 'r+')
        cache = json.load(f)
        f = open('bindex.json', 'r+')
        index = json.load(f)
        urlee.strip()
        if not urlee in list(cache) and not urlee in list(index) or fp is True:
            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(None,
                                              lambda: ydl.extract_info(urlee, download=False))
            #print(info)
            #f = open('info.json', 'w+')
            #json.dump(f, info)
            if info is None:
                await ctx.send("BAD")
                return
            if 'entries' in info and info['entries'] == []:
                await ctx.send("BAD")
                return
            #print(info['entries']['webpage_url'])
            if not isinstance(info,dict):
                await ctx.send("BAD")
                return
            if 'entries' in info:
                #print(info)
                gid = loljs[ctx.guild.id]
                index[urlee] = []
                for song in info["entries"]:
                    if song['webpage_url'] in list(cache):
                        index[urlee].append(song['webpage_url'])
                        URL_s= song['webpage_url']
                        tit = song['title']
                        thumb= song['thumbnail']
                    else:
                        cache[song['webpage_url']] = {}
                        cache[song['webpage_url']]['URL'] = song['url']
                        URL_s = cache[song['webpage_url']]['URL_s'] = song['webpage_url']
                        tit = cache[song['webpage_url']]['tit'] =   song['title']
                        thumb = cache[song['webpage_url']]['thumb'] = song['thumbnail']
                        index[urlee].append(song['webpage_url'])
                gid['que'].extend(index[urlee])

            else:
                gid = loljs[ctx.guild.id]
                cache[urlee] = {}
                cache[urlee]['URL'] =   info['url']
                URL_s = cache[urlee]['URL_s'] = info['webpage_url']
                tit = cache[urlee]['tit'] =   info['title']
                thumb = cache[urlee]['thumb'] = info['thumbnail']
                gid['que'].append(urlee)

            with open('bcache.json', 'w') as fe:
                json.dump(cache, fe)
            with open('bindex.json', 'w') as fe:
                json.dump(index, fe)

        else:
            gid = loljs[ctx.guild.id]
            if urlee in list(cache):
                if await scrap(cache[urlee]['URL']):
                    loop = asyncio.get_event_loop()
                    info = await loop.run_in_executor(None,
                                                      lambda: ydl.extract_info(urlee, download=False))
                    cache[urlee]['URL'] = info['url']
                gid['que'].append(urlee)
                URL_s = cache[urlee]['URL_s']
                tit = cache[urlee]['tit']
                thumb = cache[urlee]['thumb']
                print(gid['que'])
            else:
                if await scrap(cache[index[urlee][0]]['URL']):
                    loop = asyncio.get_event_loop()
                    info = await loop.run_in_executor(None,
                                                      lambda: ydl.extract_info(index[urlee][0], download=False))
                    cache[index[urlee][0]]['URL'] = info['url']
                gid['que'].extend(index[urlee])
                URL_s = cache[index[urlee][-1]]['URL_s']
                tit = cache[index[urlee][-1]]['tit']
                thumb = cache[index[urlee][-1]]['thumb']

            with open('bcache.json', 'w') as fe:
                json.dump(cache, fe)
            with open('bindex.json', 'w') as fe:
                json.dump(index, fe)

        ###SEND EMBED
        ###POSLE SONG KTERY SE PRDAL DO PORAD
        self.bot.loop.create_task(self.embed_ns(ctx, tit, URL_s, thumb, cache))

        ###SOME LOOPawait init STUFF
        if not await self.is_connected(ctx):
            channel = ctx.author.voice.channel
            #chl = self.bot.get_channel(channel)
            await channel.connect()


        if not loljs[ctx.guild.id]['playing']:
            loljs[ctx.guild.id]['playing'] = True

            x = asyncio.Event()

            def skipe(error=None):
                x.set()

            while True:
                if loljs[ctx.guild.id]['que']:
                    f = open('bcache.json', 'r+')
                    cache = json.load(f)
                    voice = get(self.bot.voice_clients, guild=ctx.guild)
                    x.clear()
                    fid = loljs[ctx.guild.id]
                    ###LOOP
                    ###SPRAVOVANI PRAVE HRANEHO SONGU
                    loop = fid['loop']
                    if loop:
                        if fid["crpe"] is not None:
                            if fid['shuffle']:
                                fid["crp"] += re.randint(0, len(fid['que']))
                            else:
                                fid["crp"] += 1
                            if fid["crp"] >= len(fid['que']):
                                fid["crp"] = 0
                    else:
                        if fid["crpe"] is not None:
                            if fid['shuffle']:
                                del fid['que'][fid["crp"]]
                                fid["crp"] += re.randint(0, len(fid['que']))
                            else:
                                del fid['que'][fid["crp"]]
                                if fid["crp"] == len(fid['que']):
                                    fid["crp"] = 0
                    if loljs[ctx.guild.id]['que']:
                        ###STREAM AUDIO
                        ###COD KTERY STREAMUJE VIDEO Z LINKU
                        URL = cache[fid['que'][fid["crp"]]]['URL']
                        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=skipe)
                        voice.source = discord.PCMVolumeTransformer(voice.source)
                        voice.source.volume = 0.05
                        fid["crpe"] = fid['que'][fid["crp"]]
                        ###UPDATE CRP COMMAND
                        ###UPDATNE CRP ZPRAVU S PRAVE HRAJICIM SONGEM
                        chid = fid['rpm']['chid']
                        if chid is not None:
                            chal = self.bot.get_channel(chid)
                            message = await chal.fetch_message(fid['rpm']['mid'])
                            await message.edit(embed=await self.embed_crp(ctx.guild.id, 'playing', cache))
                    else:
                        loljs[ctx.guild.id]["crpe"] = None
                        loljs[ctx.guild.id]['playing'] = False
                        print('drop it2')
                        break
                else:
                    loljs[ctx.guild.id]["crpe"] = None
                    loljs[ctx.guild.id]['playing'] = False
                    print('drop it3')
                    break
                await x.wait()


    @tasks.loop(seconds=120.0)
    async def vali(self):
        await validate(self.bot, YDL_OPTIONS)

def setup(bot):
    bot.add_cog(music(bot))