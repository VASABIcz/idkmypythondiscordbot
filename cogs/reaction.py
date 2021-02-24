###INTERACRIVE CONTROL HANDELING
###INTERAKTIVNI OVLADANI PREZ REAKCE


import discord
from discord.ext import commands, tasks
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
import json
import asyncio
import random as re
import time
from bconstant import *
global loljs
f = open('bcache.json', 'r+')
cache = json.load(f)
f = open('bindex.json', 'r+')
index = json.load(f)
class reaction(commands.Cog):
    def __init__(self, bot):
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
        self.bot = bot
        self.init = init
        self.scrap = scrap
        self.validate = validate
        self.is_connected = is_connected
        self.embed_crp = embed_crp
        self.embed_que = embed_que
        self.embed_ns = embed_ns

    f = open('bcache.json', 'r+')
    cache = json.load(f)
    f = open('bindex.json', 'r+')
    index = json.load(f)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        ###handle reaction
        gid = payload.guild_id
        await self.init(gid)
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
                        if voice is not None:
                            voice.pause()
                            if loljs[gid]['rpm']['chid'] is not None:
                                chal = self.bot.get_channel(int(loljs[gid]['rpm']['chid']))
                                message = await chal.fetch_message(loljs[gid]['rpm']['mid'])
                                try:
                                    await message.edit(embed=await self.embed_crp(gid, 'paused', cache))
                                except:
                                    pass


                    if payload.emoji.name == '▶️':
                        guild = self.bot.get_guild(gid)
                        voice = get(self.bot.voice_clients, guild=guild)
                        if voice is not None:
                            voice.resume()
                            if loljs[gid]['rpm']['chid'] is not None:
                                chal = self.bot.get_channel(int(loljs[gid]['rpm']['chid']))
                                message = await chal.fetch_message(loljs[gid]['rpm']['mid'])
                                try:
                                    await message.edit(embed=await self.embed_crp(gid, 'playing'))
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
                    await message.edit(embed=await self.embed_que(gid, nam, cache))



def setup(bot):
    bot.add_cog(reaction(bot))