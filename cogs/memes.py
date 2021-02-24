from discord.ext import commands
import requests

class memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=['mem'])
    async def meme(self, ctx, *, imp):
        try:
            mem = requests.get(f'https://meme-api.herokuapp.com/gimme/{imp}')
            js = mem.json()
            await ctx.channel.send(js['url'])
        except:
            pass

    @commands.command()
    async def animeme(self, ctx):
        await ctx.channel.send('D:')

def setup(bot):
    bot.add_cog(memes(bot))