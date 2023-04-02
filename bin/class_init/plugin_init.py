from discord.ext import commands

class plugin_init(commands.Cog) :
    def __init__(self, bot) :
        self.bot = bot