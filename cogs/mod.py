import discord
from discord import app_commands
from discord.ext import commands

from embeds.error import error_embed
from embeds.success import success_embed


class Mod(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


async def setup(bot: commands.Bot):
    await bot.add_cog(Mod(bot=bot))
