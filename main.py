import os
import sys
import getopt #input args
import psutil
import asyncio
import configparser
import discord
from discord.ext import commands
from bin import ctc ,source, ctt, token
from bin.class_init.plugin_init import plugin_init
#===============app start
argv = sys.argv[1:]
arg_token = None
try:
    opts, args = getopt.getopt(argv,"ht:",["token="])
except getopt.GetoptError:
    print ('main.py -t <token>')
    sys.exit(2)
for opt, arg in opts:
      if opt == '-h':
         print ('main.py -t <token>')
         sys.exit(0)
      elif opt in ("-t", "--token"):
         arg_token = arg
#=================
config = configparser.ConfigParser()
config.read("./config/config.ini")
Command_prefix = ["!"]
listenner_port = (config["client"].getint("listenner_port"))
intents = discord.Intents.all()#(value=137442520128)
bot = commands.Bot(command_prefix=Command_prefix, intents=intents)


#=================
@bot.command(name="shutdown")
async def shutdown(ctx :commands.Context):
    await bot.change_presence(status=discord.Status.invisible)
    await ctx.send(f"> {source.off_cv()}")
    await bot.close()

@bot.command(name="ping")
async def ping(ctx :commands.Context):
    #==========cpu, ram useage
    # CPU usage
    CPU_use = psutil.cpu_percent(interval=0.3)
    # Memory usage
    RAM_use = psutil.virtual_memory()[2]
    #ping
    ping = round(bot.latency*1000)
    #==========embed_color

    e_color = 0x59ff00

    #==========
    embed = (discord.Embed(title=u'🍵{0.user.name}'.format(bot),
                               description=f'```ini\n[system/INFO]                                            \n```',
                               color=e_color)
                 .add_field(name='💠CPU usage', value=f"{CPU_use}%")
                 .add_field(name='🧱RAM usage', value=f"{RAM_use}%")
                 .add_field(name='📡ping', value=f"{ping}-ms")
                 .set_author(icon_url="https://cdn.discordapp.com/emojis/1028895182290161746.webp", name=f"CORN Studio"))

    await ctx.send(embed=embed)
    
    ctc.printYellow(f'{ctt.time_now()}:INFO:ping:[{ping}]-ms=>[{bot.latency*1000}]-us\n')
#============================================================
class commands_error_handler(plugin_init) :
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        embed = discord.Embed(title="Command ERROR :", description=f"{error}", color=0xf6ff00)
        await ctx.reply(embed=embed)
        ctc.printYellow(f"{ctt.time_now()}:ERROR:{error}\n")
async def load_error_handler():
    await bot.add_cog(commands_error_handler(bot))

async def load_extensions() :
    for cog_files in os.listdir("./plugins") :
        if cog_files.endswith(".py") :
            await bot.load_extension(f"plugins.{cog_files[:-3]}")
        elif cog_files.endswith(".pyc") :
            await bot.load_extension(f"plugins.{cog_files[:-4]}")

@bot.command(name="load",description="Load plugin.")
@commands.is_owner()
async def load(ctx, extension):
    await ctx.message.add_reaction('✅')
    await bot.load_extension(f'plugins.{extension}')
    await ctx.send(f"succeed load `{extension}` plugin")

@bot.command(name="unload",description="Unload plugin.")
@commands.is_owner()
async def unload(ctx, extension):
    if extension == "commands_error_handler" :
        await ctx.send("Can't unload this plugin.")
    else:
        await ctx.message.add_reaction('⚠️')
        await bot.unload_extension(f'plugins.{extension}')
        await ctx.send(f"succeed unload `{extension}` plugin")

@bot.command(name="reload",description="Reload plugin.")
@commands.is_owner()
async def reload(ctx, extension):
    await ctx.message.add_reaction('🔄')
    await bot.reload_extension(f'plugins.{extension}')
    await ctx.send(f"succeed reload `{extension}` plugin")



@bot.event
async def on_ready():
    os.system("cls")
    ctc.printDarkSkyBlue("Discord Bot Server [版本 c.1.0.1]\n")
    ctc.printBlue("Copyright (c) 2023 FUBUKINGFOX. 著作權所有，並保留一切權利。\n")
    ctc.printGreen(u'Logged in as:\n'.format(bot))
    ctc.printPink(u'{0.user.name}\n'.format(bot))
    ctc.printYellowBlue(u'{0.user.id}\n'.format(bot))
    try :
        slash_cmd = await bot.tree.sync()
        ctc.printBlue(f"{ctt.time_now()}:INFO :upload {len(slash_cmd)} slash command(s)\n")
    except Exception as error :
        print("failed to upload slash command(s)")
        print(f"Exception:\n{error}")
    try :
        channel = bot.get_channel(listenner_port)
    except Exception:
        pass
    await channel.send(":minidisc::{0.user.name}`{0.user.id}`".format(bot))
    ACT = discord.Activity(type=discord.ActivityType.playing, name="")
    await bot.change_presence(activity=ACT, status=discord.Status.online)


async def main(token):
    async with bot :
        await load_extensions()
        await load_error_handler()
        await bot.start(token)

if __name__ == "__main__" :
    ctc.printDarkGray(f"{ctt.time_now()} connecting to discord...\n")
    asyncio.run(main(token.token(arg_token)))
