from datetime import timedelta

import discord
from discord.ext import commands


class Moderate(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_command_error(
        self, _: discord.ApplicationContext, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingPermissions) or isinstance(
            error, commands.BotMissingPermissions
        ):
            return

    @commands.slash_command(
        name="청소", description="입력된 개수만큼 메시지를 제거합니다."
    )
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    async def clear(
        self,
        ctx: discord.ApplicationContext,
        amount: discord.Option(
            discord.SlashCommandOptionType.integer,
            name="개수",
            description="지울 개수",
            min_value=1,
            max_value=99,
            required=True,
        ),
    ):
        await ctx.channel.purge(limit=amount)
        await ctx.respond(f"{amount}건에 메시지를 제거했습니다.", delete_after=10.0)

    @commands.slash_command(name="역할", description="유저의 역할을 관리합니다.")
    async def roles(
        self,
        ctx: discord.ApplicationContext,
        whether: discord.Option(
            discord.SlashCommandOptionType.string,
            name="여부",
            description="추가/제거 여부",
            choices=["추가", "제거"],
            required=True,
        ),
        member: discord.Option(
            discord.Member, name="맴버", description="추가/제거할 맴버", required=True
        ),
        role: discord.Option(
            discord.Role, name="역할", description="추가/제거할 역할", required=False
        ),
    ):
        if "추가" in whether:
            await member.add_roles(role)
            await ctx.respond(
                f"{member.mention}님에게 {role.mention}를 {whether}했습니다.",
                ephemeral=False,
            )
        else:
            await member.remove_roles(role)
            await ctx.respond(
                f"{member.mention}님에게 {role.mention}를 {whether}했습니다.",
                ephemeral=False,
            )

    @commands.slash_command(name="밴", description="유저를 밴합니다.")
    @commands.has_permissions(ban_members=True)
    async def ban(
        self,
        ctx: discord.ApplicationContext,
        member: discord.Option(
            discord.Member, name="맴버", description="밴할 유저", required=True
        ),
    ):
        await member.ban()
        await ctx.respond(f"{member.mention}님을 밴했습니다.")

    @commands.slash_command(name="킥", description="유저를 킥합니다.")
    @commands.has_permissions(kick_members=True)
    async def kick(
        self,
        ctx: discord.ApplicationContext,
        member: discord.Option(
            discord.Member, name="맴버", description="킥할 유저", required=True
        ),
    ):
        await member.kick()
        await ctx.respond(f"{member.mention}님을 킥했습니다.")

    @commands.slash_command(
        name="타임아웃", description="유저에게 타임아웃을 적용하거나 해제합니다."
    )
    async def timeout(
        self,
        ctx: discord.ApplicationContext,
        member: discord.Option(
            discord.Member, name="맴버", description="타임아웃할 맴버", required=True
        ),
        duration: discord.Option(
            discord.SlashCommandOptionType.integer,
            name="기간",
            description="타임아웃 기간 (일)",
            min_value=0,
            max_value=28,
            required=True,
        ),
    ):
        await member.timeout_for(duration=timedelta(days=duration))

        if duration == 0:
            await ctx.respond(f"{member.mention}님의 타임아웃을 제거했습니다.")
        else:
            await ctx.respond(
                f"{member.mention}님에게 {duration}일만큼 타임아웃했습니다."
            )

    @commands.slash_command(
        name="슬로우모드", description="채널에 슬로우모드를 적용하거나 해제합니다."
    )
    @commands.has_permissions(manage_channels=True)
    @commands.guild_only()
    async def slowmode(
        self,
        ctx: discord.ApplicationContext,
        duration: discord.Option(
            discord.SlashCommandOptionType.integer,
            min_value=0,
            max_value=21600,
            name="기간",
            description="슬로우모드 기간(초)",
            required=True,
        ),
    ):
        await ctx.channel.edit(slowmode_delay=timedelta(seconds=duration).seconds)
        await ctx.respond(f"{ctx.channel.name}의 슬로우모드를 적용했습니다.")


def setup(bot: commands.Bot):
    bot.add_cog(Moderate(bot=bot))
