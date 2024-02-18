from datetime import datetime
from time import mktime

import discord
from discord import app_commands
from discord.ext import commands
from embeds.extra.serverinfo import *
from embeds.extra.userinfo import *


class General(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.start_time = datetime.now()

    @app_commands.command(name="핑", description="봇의 응답속도를 확인합니다.")
    async def ping(self, interaction: discord.Interaction):
        total_seconds = (datetime.now() - self.start_time).total_seconds()
        to_start_time = round(mktime(self.start_time.timetuple()))

        uptime = f"<t:{round(to_start_time - total_seconds)}:R>"
        latency = f"``{round(self.bot.latency * 1000)}``ms"
        shard = f"``{self.bot.shard_count}``개"

        await interaction.response.defer(thinking=True, ephemeral=False)

        embed = discord.Embed()
        embed.set_footer(
            text=interaction.user.name, icon_url=interaction.user.display_avatar
        )
        embed.add_field(name="🏓 응답속도", value=latency, inline=True)
        embed.add_field(name="⌛ 업타임", value=uptime, inline=True)
        embed.add_field(name="💻 샤드", value=shard, inline=True)

        await interaction.followup.send(embed=embed, ephemeral=False)

    @app_commands.command(name="유저", description="유저 정보를 불러옵니다.")
    @app_commands.rename(member="유저")
    @app_commands.describe(member="정보를 가져올 유저")
    async def userinfo(
        self, interaction: discord.Interaction, member: discord.Member = None
    ):
        if member is None:
            member = interaction.user

        await interaction.response.defer(thinking=True, ephemeral=False)
        await interaction.followup.send(
            embed=await userinfo(member=member), ephemeral=False
        )

    @app_commands.command(name="서버", description="서버 정보를 불러옵니다.")
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild

        await interaction.response.defer(thinking=True, ephemeral=False)
        await interaction.followup.send(
            embed=await serverinfo(interaction=interaction, guild=guild),
            ephemeral=False,
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot=bot))
