from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands
from utils.unix import to_unix


class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="핑", description="봇의 응답속도를 표시합니다.")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(
            f":ping_pong: Pong!(``{latency}ms``)",
            ephemeral=True,
        )

    @app_commands.command(name="업타임", description="봇의 업타임를 보여줍니다.")
    async def uptime(self, interaction: discord.Interaction):
        t1 = datetime.now() - self.start_time
        t2_sec = t1.total_seconds()

        st_unix = to_unix(self.start_time.timetuple())

        t3 = round(st_unix - t2_sec)
        t3_unix = f"<t:{t3}:R>"

        await interaction.response.defer(ephemeral=False, thinking=True)
        await interaction.followup.send(
            f"{t3_unix}에 마지막으로 꺼졌습니다.", ephemeral=False
        )

    @app_commands.command(name="유저정보", description="유저의 정보를 불러옵니다.")
    @app_commands.rename(member="맴버")
    @app_commands.describe(member="맴버")
    async def userinfo(
        self, interaction: discord.Interaction, member: discord.Member = None
    ):
        if member is None:
            member = interaction.user

        createdAt = to_unix(date=member.created_at)
        joinedAt = to_unix(date=member.joined_at)

        status: dict = {
            discord.Status.online: "온라인",
            discord.Status.idle: "자리비움",
            discord.Status.dnd: "다른 용무 중",
            discord.Status.offline: "오프라인",
        }
        pfp = member.display_avatar

        embed = discord.Embed(color=member.color)
        embed.set_author(name=member.name, icon_url=pfp)
        embed.set_thumbnail(url=pfp)

        embed.add_field(name="ID", value=f"``{member.id}``", inline=False)
        embed.add_field(
            name="상태",
            value=f"{status[member.status]}",
            inline=False,
        )
        embed.add_field(
            name="생성일", value=f"<t:{createdAt}> (<t:{createdAt}:R>)", inline=False
        )
        embed.add_field(
            name="접속일", value=f"<t:{joinedAt}> (<t:{joinedAt}:R>)", inline=False
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="서버정보", description="서버 정보를 불러옵니다.")
    async def serverinfo(self, interaction: discord.Interaction):
        server = interaction.guild

        createdAt = to_unix(date=server.created_at)

        embed = discord.Embed()
        embed.set_author(name=server.name)

        embed.add_field(
            name="소유자",
            value=f"{server.owner.mention} (``{server.owner_id}``)",
            inline=False,
        )
        embed.add_field(name="ID", value=server.id, inline=False)
        embed.add_field(
            name="생성일", value=f"<t:{createdAt}> (<t:{createdAt}:R>)", inline=False
        )
        embed.add_field(name="맴버 수", value=f"{server.member_count}명", inline=True)
        embed.add_field(
            name="채널 수",
            value=f"{len(server.text_channels) + len(server.voice_channels)}개",
            inline=True,
        )
        embed.add_field(name="역할 수", value=f"{len(server.roles)}개", inline=True)
        embed.add_field(
            name="부스트 수",
            value=f"{server.premium_subscription_count}개",
            inline=True,
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="아바타", description="유저의 아바타를 보여줍니다.")
    @app_commands.rename(member="맴버")
    @app_commands.describe(member="맴버")
    async def avatar(
        self, interaction: discord.Interaction, member: discord.Member = None
    ):
        if member is None:
            member = interaction.user

        img = member.display_avatar

        button = discord.Button(
            label="바로가기",
            style=discord.ButtonStyle.link,
            url=img.url,
            emoji="🔗",
        )
        view = discord.View()
        view.add_item(button)

        embed = discord.Embed(color=member.color)

        embed.set_author(name=member.name, icon_url=img)
        embed.set_image(url=img)

        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @app_commands.command(name="배너", description="유저의 배너를 보여줍니다.")
    @app_commands.rename(member="맴버")
    @app_commands.describe(member="맴버")
    async def banner(
        self, interaction: discord.Interaction, member: discord.Member = None
    ):
        if member is None:
            member = interaction.user

        bnr = member.banner

        if bnr is None:
            return await interaction.response.send_message(
                f"{member.mention}님은 배너가 없습니다.", ephemeral=False
            )

        button = discord.Button(
            label="바로가기",
            style=discord.ButtonStyle.link,
            url=bnr.url,
            emoji="🔗",
        )
        view = discord.View()
        view.add_item(button)

        embed = discord.Embed(color=member.color)

        embed.set_author(name=member.name)
        embed.set_image(url=bnr)

        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot=bot))
