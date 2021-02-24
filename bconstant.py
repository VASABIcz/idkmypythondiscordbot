import discord
from discord.ext import commands, tasks
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
import json
import asyncio
import random as re
import time
import requests

loljs = {}
YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': True,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
}
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}


async def init(ctx):
    if ctx not in loljs:
        if isinstance(ctx, int):
            if not ctx in list(loljs):
                loljs[ctx] = {}
                loljs[ctx]['loop'] = False
                loljs[ctx]['que'] = []
                loljs[ctx]["crp"] = 0
                loljs[ctx]['playing'] = False
                loljs[ctx]['shuffle'] = False
                loljs[ctx]["crpe"] = None
                loljs[ctx]['rpm'] = {}
                loljs[ctx]['rpm']['mid'] = None
                loljs[ctx]['rpm']['chid'] = None
                loljs[ctx]['quem'] = {}
                loljs[ctx]['quem']['mid'] = None
                loljs[ctx]['quem']['chid'] = None
                loljs[ctx]['quem']['pg'] = None
        else:
            if not ctx.guild.id in list(loljs):
                loljs[ctx.guild.id] = {}
                loljs[ctx.guild.id]['loop'] = False
                loljs[ctx.guild.id]['que'] = []
                loljs[ctx.guild.id]["crp"] = 0
                loljs[ctx.guild.id]['playing'] = False
                loljs[ctx.guild.id]['shuffle'] = False
                loljs[ctx.guild.id]["crpe"] = None
                loljs[ctx.guild.id]['rpm'] = {}
                loljs[ctx.guild.id]['rpm']['mid'] = None
                loljs[ctx.guild.id]['rpm']['chid'] = None
                loljs[ctx.guild.id]['quem'] = {}
                loljs[ctx.guild.id]['quem']['mid'] = None
                loljs[ctx.guild.id]['quem']['chid'] = None
                loljs[ctx.guild.id]['quem']['pg'] = None


async def is_connected(ctx):
    voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()


# EXTRAHOVANI FUCKNCNI DOBU SONGU
async def scrap(URL):
    if 'expire=' in URL:
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
    else:
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


async def ahoj(n, lil, filee, ydl):
    if not "//cf-" in filee[lil[n]]['URL']:
        if await scrap(filee[lil[n]]['URL']):
            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(None, lambda: ydl.extract_info(filee[lil[n]]['URL_s'], download=False))
            if info is None:
                del filee[lil[n]]
                return
            filee[lil[n]]['URL'] = info['url']
            with open('bcache.json', 'w+') as fe:
                json.dump(filee, fe)

            # print(f'validated cache {lil[n]}')
            # if str(requests.get(filee[lil[n]]['URL'])) == "<Response [403]>":
            #    loop = asyncio.get_event_loop()
            #    info = await loop.run_in_executor(None, lambda: ydl.extract_info(filee[lil[n]]['URL_s'], download=False))
            #    if info is None:
            #        del filee[lil[n]]
            #        return
            #    filee[lil[n]]['URL'] = info['url']
            #    with open('cache.json', 'w') as fe:
            #        json.dump(filee, fe)
            #    print(f'validated cache {lil[n]}')

###COMAND PRO KONTROLU FUNKCNOSTI LINKU
async def validate(bot, opt):
    ydl = YoutubeDL(opt)
    ###VALIDATE ALL LINKS WHILE PLAYING ANOTHER SONG TO BYPASS USER WAITING FOR VALIDATION

    # VALIDATE CACHE
    with open('bcache.json', 'r+') as f:
        filee = json.load(f)
    if filee != {}:
        lil = list(filee)
        for n in range(len(filee)):
            try:
                bot.loop.create_task(ahoj(n, lil, filee, ydl))
            except:
                pass

async def embed_crp(gid, play, cache):
    embed = discord.Embed(title=cache[loljs[gid]["crpe"]]['tit'],
                          url=cache[loljs[gid]["crpe"]]['URL_s'],
                          colour=0xe91e63)
    embed.set_author(name='VASABI',
                     url='https://github.com/VASABIcz/Simple-discord-music-bot',
                     icon_url='https://i.ytimg.com/vi_webp/xeA7VQE_R1k/maxresdefault.webp')
    embed.set_thumbnail(url=cache[loljs[gid]["crpe"]]['thumb'])
    embed.add_field(name='status', value=play, inline=False)
    embed.add_field(name='commands', value='_', inline=False)
    embed.add_field(name='⏸️/▶️', value='**`pause/resume`**', inline=True)
    embed.add_field(name='❗️', value='**`disconnect`**', inline=True)
    embed.add_field(name='⏩', value='**`skip`**',
                    inline=True)  # **`aaaaaaa`**
    return embed


async def embed_que(gid, nam, cache):
    qee = loljs[gid]['que']
    embed = discord.Embed(title="QUE (:", description="Song que",
                          colour=0xe91e63)
    embed.set_author(name='VASABI', url='https://github.com/VASABIcz/Simple-discord-music-bot',
                     icon_url='https://i.ytimg.com/vi_webp/xeA7VQE_R1k/maxresdefault.webp')
    for i in range(5):
        rov = i + (nam * 5) - 5
        try:
            embed.add_field(name=cache[qee[int(rov)]]['tit'], value=str(rov), inline=False)
        except:
            pass
    embed.set_footer(text=f"page<{nam}>")
    return embed


async def embed_ns(ctx, tit, URL_s, thumb, cache):
    embed = discord.Embed(title=tit, url=URL_s, description='Added to que:',
                          color=0xe91e63)
    embed.set_author(name='VASABI', url='https://github.com/VASABIcz/Simple-discord-music-bot',
                     icon_url='https://i.ytimg.com/vi_webp/xeA7VQE_R1k/maxresdefault.webp')
    embed.set_thumbnail(url=thumb)
    if loljs[ctx.guild.id]["crpe"]:
        embed.set_footer(text=f"Position in que: {len(loljs[ctx.guild.id]['que']) - 1}")
    else:
        if loljs[ctx.guild.id]['loop']:
            embed.set_footer(text=f"Position in que: {len(loljs[ctx.guild.id]['que']) - 1}")
        else:
            embed.set_footer(text="Now playing")
    await ctx.send(embed=embed)
