from random import *

import discord
from discord import app_commands
from discord.ext import commands

from embeds.error import error_embed
from embeds.image import image_embed
from function.meme import *
from function.nyehuing import make_nyehuing


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="강아지", description="강아지 사진을 보내줍니다.")
    async def dog(self, interaction: discord.Interaction):
        r = await dog()

        await interaction.response.defer(thinking=True, ephemeral=False)
        await interaction.followup.send(embed=await image_embed(url=r), ephemeral=False)

    @app_commands.command(name="고양이", description="고양이 사진을 보내줍니다.")
    async def cat(self, interaction: discord.Interaction):
        r = await cat()

        await interaction.response.defer(thinking=True, ephemeral=False)
        await interaction.followup.send(embed=await image_embed(url=r), ephemeral=False)

    @app_commands.command(name="주사위", description="주사위를 굴립니다.")
    async def dice(self, interaction: discord.Interaction):
        r = randint(1, 6)

        await interaction.response.defer(thinking=True, ephemeral=True)
        await interaction.followup.send(f"🎲 {r}", ephemeral=True)

    @app_commands.command(name="녜힁", description="녜힁을 생성합니다.")
    @app_commands.rename(length="길이")
    @app_commands.describe(length="생성할 길이")
    async def nyehuing(self, interaction: discord.Interaction, length: int):
        if not 0 < length < 16:
            await interaction.response.defer(thinking=True, ephemeral=True)
            return await interaction.followup.send(
                embed=await error_embed(
                    description="1개 이상 16개 이하로 입력해주세요."
                ),
                ephemeral=True,
            )

        r = make_nyehuing(length=length)
        await interaction.response.defer(thinking=True, ephemeral=True)
        await interaction.followup.send(r, ephemeral=True)

    @app_commands.command(name="짤", description="랜덤한 짤을 보내줍니다.")
    @app_commands.choices(
        category=[
            app_commands.Choice(name="발차기", value="kick"),
            app_commands.Choice(name="허그", value="hug"),
            app_commands.Choice(name="키스", value="kiss"),
            app_commands.Choice(name="흔들기", value="wave"),
            app_commands.Choice(name="하이파이브", value="highfive"),
            app_commands.Choice(name="윙크", value="wink"),
            app_commands.Choice(name="댄스", value="dance"),
            app_commands.Choice(name="네코", value="neko"),
            app_commands.Choice(name="시노부", value="shinobu"),
            app_commands.Choice(name="때리기", value="slap"),
            app_commands.Choice(name="울기", value="cry"),
        ]
    )
    @app_commands.rename(category="목록")
    @app_commands.describe(category="짤 목록")
    async def meme(
        self, interaction: discord.Interaction, category: app_commands.Choice[str]
    ):
        r = await waifu(category=category.value)

        await interaction.response.defer(thinking=True, ephemeral=False)
        await interaction.followup.send(embed=await image_embed(url=r), ephemeral=False)

    @app_commands.command(name="골라", description="봇이 골라줍니다.")
    @app_commands.rename(query="항목")
    @app_commands.describe(query="항목 (ex. A/B)")
    async def choose(self, interaction: discord.Interaction, query: str):
        a = query.split("/")
        r = choice(a)

        await interaction.response.defer(thinking=True, ephemeral=True)
        await interaction.followup.send(r, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Fun(bot=bot))
