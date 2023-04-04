import os
import sys
import getopt #input args
import asyncio
import discord
from discord.ext import commands
from bin import ctc ,source, ctt, token
from bin.class_init import plugin_init
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

Command_prefix = ["!"]
listenner_port = ()
intents = discord.Intents(value=137442520128)
bot = commands.Bot(command_prefix=Command_prefix, intents=intents ,help_command=None)

#=================
ctc.printDarkGray(f"{ctt.time_now()} connecting to discord...")
#=================
@bot.command(name="shutdown")
async def shutdown(ctx :commands.Context):
    await bot.change_presence(status=discord.Status.invisible)
    await ctx.send(f"> {source.off_cv()}")
    await bot.close()

@bot.command(name="ping")
async def ping(ctx :commands.Context):
    await ctx.send()


#============================================================
class commands_error_handler(plugin_init) :
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        ctc.printRed(f"{ctt.time_now()}:ERROR:{error}")
        embed = discord.Embed(title="Command ERROR :", description=f"{error}", color=0xf6ff00)
        await ctx.reply(embed=embed)
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
    ctc.printDarkSkyBlue("Discord Bot Server [版本 c.1.0.0]")
    ctc.printBlue("[MIT License]Copyright (c) 2023 FUBUKINGFOX. 著作權所有，並保留一切權利。")
    ctc.printGreen(u'Logged in as:\n'.format(bot))
    ctc.printPink(u'{0.user.name}\n'.format(bot))
    ctc.printYellowBlue(u'{0.user.id}\n'.format(bot))
    channel = bot.get_channel(listenner_port)
    await channel.send(":minidisc::{0.user.name}`{0.user.id}`".format(bot))
    ACT = discord.Activity(type=discord.ActivityType.playing, name="")
    bot.change_presence(activity=ACT, status=discord.Status.online)


async def main(token: str):
    async with bot :
        await load_extensions()
        await load_error_handler()
        await bot.start(token)

if __name__ == "__main__" :
    asyncio.run(main(token.token(arg_token)))