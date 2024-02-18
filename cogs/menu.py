import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View
from embeds.extra.avatar import avatar
from embeds.extra.userinfo import userinfo
from inko import Inko


class Menu(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

        self.search_userinfo_menu = app_commands.ContextMenu(
            name="유저정보 조회하기",
            callback=self.search_userinfo,
        )
        self.bot.tree.add_command(self.search_userinfo_menu)

        self.search_avatar_menu = app_commands.ContextMenu(
            name="프로필 사진 조회하기",
            callback=self.search_avatar,
        )
        self.bot.tree.add_command(self.search_avatar_menu)

        self.en_to_kr_menu = app_commands.ContextMenu(
            name="한타로 변환하기",
            callback=self.en_trans_ko,
        )
        self.bot.tree.add_command(self.en_to_kr_menu)

        self.ko_to_en_menu = app_commands.ContextMenu(
            name="영타로 변환하기",
            callback=self.ko_trans_en,
        )
        self.bot.tree.add_command(self.ko_to_en_menu)

    async def search_userinfo(
        self, interaction: discord.Interaction, member: discord.Member = None
    ):
        if member is None:
            member = interaction.user

        await interaction.response.defer(thinking=True, ephemeral=False)
        await interaction.followup.send(
            embed=await userinfo(member=member), ephemeral=False
        )

    async def en_trans_ko(
        self, interaction: discord.Interaction, message: discord.Message
    ):
        inko = Inko()
        result: str = inko.en2ko(message.content)

        await interaction.response.defer(thinking=True, ephemeral=True)
        await interaction.followup.send(result, ephemeral=True)

    async def ko_trans_en(
        self, interaction: discord.Interaction, message: discord.Message
    ):
        inko = Inko()
        result: str = inko.ko2en(message.content)

        await interaction.response.defer(thinking=True, ephemeral=True)
        await interaction.followup.send(result, ephemeral=True)

    async def search_avatar(
        self, interaction: discord.Interaction, member: discord.Member = None
    ):
        if member is None:
            member = interaction.user

        btn = Button(label="바로가기", url=member.display_avatar.url, emoji="🔗")
        view = View()
        view.add_item(btn)

        await interaction.response.defer(thinking=True, ephemeral=True)
        await interaction.followup.send(
            embed=await avatar(member=member), ephemeral=True, view=view
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Menu(bot=bot))
