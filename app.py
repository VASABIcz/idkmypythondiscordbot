import os
from dotenv import load_dotenv
from os import listdir
from bconstant import *
import ast
import discord
import io
from discord import File
from discord.ext import commands


def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)
#os.environ['PYTHONASYNCIODEBUG'] = '1'
#logging.basicConfig(level=logging.DEBUG)
#warnings.resetwarnings()
# TODO Checks guild only ...
#
# known bugs
# ¯\_(ツ)_/¯
# TODO per guild prefix


load_dotenv('.env')
PREF = os.environ['PREF']
TOKEN = os.environ['TOKEN']
intents = discord.Intents()
intents = intents.all()
bot = commands.Bot(command_prefix=PREF, intents=intents)

@bot.command(brief="reload cogs")
@commands.is_owner()
async def reload(ctx, name):
    bot.reload_extension(f'cogs.{name}')
    await ctx.channel.send('cog reloaded')

@bot.command(brief="load cogs")
@commands.is_owner()
async def load(_ctx, name):
    bot.load_extension(f'cogs.{name}')


@bot.command(brief="simple eval", name='eval')
@commands.is_owner()
async def _eval(ctx, *, cmd):
    fn_name = "_eval_expr"
    cmd = cmd.strip("` ")
    # add a layer of indentation
    cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
    # wrap in async def body
    body = f"async def {fn_name}():\n{cmd}"
    parsed = ast.parse(body)
    body = parsed.body[0].body
    insert_returns(body)
    env = {
        'bot': ctx.bot,
        'discord': discord,
        'commands': commands,
        'ctx': ctx,
        '__import__': __import__,
        'loljs': loljs,
        'FFMPEG_OPTIONS': FFMPEG_OPTIONS
    }
    exec(compile(parsed, filename="<ast>", mode="exec"), env)
    result = (await eval(f"{fn_name}()", env))
    f = io.StringIO(str(result))
    await ctx.channel.send(content="yep", file=File(fp=f, filename="output.txt"))
    try:
        await ctx.send(result)
    except:
        pass

#@bot.command()
#async def covert(ctx, *, cmd):
#    cmd = str(cmd)
#    cmd = cmd.replace("print", "await ctx.channel.send")
#    cmd = cmd.replace("input", "await bot.wait_for('message')")
#    await ctx.send(cmd)

@bot.command()
async def me(ctx, mem):
    for i in ctx.guild.emojis:
        if str(mem) in str(i):
            await ctx.channel.send(i)
            break


@bot.command()
async def ping(ctx):
    await ctx.send(f'**Pong!** `{bot.latency}`')


#@bot.command()
#async def click(ctx, x: int, y: int):
#    _click(x, y)


#@bot.event
#async def on_command_error(ctx, error):
#    webhook = DiscordWebhook(
#        url='https://discord.com/api/webhooks/797142718777262121/ciIaNQ-hBMIS9ZGbCCpPoDSTT1lvKQukYy4RIJTtxKB3Ue9k_RIvh-FFAR1sUKk6ooaV',
#        content=f'{ctx.author} \n {ctx.guild} \n {str(error)}')
#    response = webhook.execute()


# ##NAPISE KDYZ JE BOT PRIPRAVEN K POUZIVANI


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('---------------------')
    activity = discord.Game(name=f"{PREF}help")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    files = listdir('cogs')
    bot.load_extension('jishaku')
    for n in files:
        if n != '__pycache__':
            if '#' not in n:
                bot.load_extension(f'cogs.{n.replace(".py", "")}')


# ##DISCORD BOT TOKEN
bot.run(TOKEN)
