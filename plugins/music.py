
from bin.class_init.plugin_init import plugin_init
class music(plugin_init):
    pass


async def setup(bot):
    await bot.add_cog(music(bot))