import imp

import discord
from discord.ext import commands
from discord.ui import Button, View

from function.unix import datetime_to_unix


class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="핑", description="봇의 응답속도를 표시합니다.")
    async def ping(self, ctx: discord.ApplicationContext):
        latency = round(self.bot.latency * 1000)
        await ctx.respond(
            f":ping_pong: Pong!(``{latency}ms``)",
            ephemeral=True,
        )

    @commands.slash_command(name="유저정보", description="유저의 정보를 불러옵니다.")
    async def userinfo(
        self,
        ctx: discord.ApplicationContext,
        member: discord.Option(
            discord.Member,
            name="맴버",
            description="정보를 표시할 맴버",
            required=False,
        ),
    ):
        if member is None:
            member = ctx.author

        createdAt = datetime_to_unix(date=member.created_at)
        joinedAt = datetime_to_unix(date=member.joined_at)

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

        embed.add_field(name="ID", value=member.id, inline=False)
        embed.add_field(
            name="상태",
            value=f"📱 ``{status[member.mobile_status]}``\n🌐 ``{status[member.web_status]}``\n🖥️ ``{status[member.desktop_status]}``",
            inline=False,
        )
        embed.add_field(
            name="생성일", value=f"<t:{createdAt}> (<t:{createdAt}:R>)", inline=False
        )
        embed.add_field(
            name="접속일", value=f"<t:{joinedAt}> (<t:{joinedAt}:R>)", inline=False
        )

        await ctx.respond(embed=embed, ephemeral=False)

    @commands.slash_command(name="서버정보", description="서버 정보를 가져옵니다.")
    @commands.guild_only()
    async def serverinfo(self, ctx: discord.ApplicationContext):
        server = ctx.guild
        createdAt = datetime_to_unix(date=server.created_at)

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

        await ctx.respond(embed=embed)

    @commands.slash_command(name="프사", description="유저의 프사를 보여줍니다.")
    async def avatar(
        self,
        ctx: discord.ApplicationContext,
        member: discord.Option(
            discord.Member,
            name="맴버",
            description="프사가 보여질 맴버",
            required=False,
        ),
    ):
        if member is None:
            member = ctx.author
        pfp = member.display_avatar

        button = Button(
            label="바로가기",
            style=discord.ButtonStyle.link,
            url=pfp.url,
            emoji="🔗",
        )
        view = View()
        view.add_item(button)

        embed = discord.Embed(color=member.color)

        embed.set_author(name=member.name, icon_url=pfp)
        embed.set_image(url=pfp)

        await ctx.response.send_message(embed=embed, view=view, ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(General(bot=bot))
