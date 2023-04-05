import discord
from discord import app_commands
from bin.class_init.plugin_init import plugin_init
class test(plugin_init):
    @app_commands.command(name="test")
    async def _test(self, itn: discord.Interaction):
        await itn.response.send_message("test")

async def setup(bot):
    await bot.add_cog(test(bot))