from datetime import timedelta

import discord
from discord.ext import commands


class Moderate(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

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
            max_value=100,
            required=True,
        ),  # type: ignore
    ):
        await ctx.channel.purge(limit=amount)
        await ctx.respond(f"{amount}건에 메시지를 제거했습니다.", delete_after=5.0)

    roles = discord.SlashCommandGroup(name="역할", description="역할을 관리합니다.")

    @roles.command(name="추가", description="역할를 추가합니다.")
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def addrole(
        self,
        ctx: discord.ApplicationContext,
        member: discord.Option(discord.Member, name="맴버", description="추가할 유저", required=True),  # type: ignore
        role: discord.Option(discord.Role, name="역할", description="추가할 역할", required=True),  # type: ignore
    ):
        if role.name == "@everyone" or role.name == "@here":
            return

        await member.add_roles(role)

        await ctx.respond(
            f"{member.name}님에게 {role.name}를 추가했습니다.", ephemeral=False
        )

    @roles.command(name="제거", description="역할를 제거합니다.")
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def removerole(
        self,
        ctx: discord.ApplicationContext,
        member: discord.Option(discord.Member, name="맴버", description="제거할 유저", required=True),  # type: ignore
        role: discord.Option(discord.Role, name="역할", description="제거할 역할", required=True),  # type: ignore
    ):
        if role.name == "@everyone" or role.name == "@here":
            return

        await member.remove_roles(role)

        await ctx.respond(
            f"{member.name}님에게 {role.name}를 제거했습니다.", ephemeral=False
        )

    @commands.slash_command(name="밴", description="유저를 서버에서 밴합니다.")
    @commands.has_permissions(ban_members=True)
    async def ban(
        self,
        ctx: discord.ApplicationContext,
        member: discord.Option(
            discord.Member, name="맴버", description="밴할 유저", required=True
        ),  # type: ignore
        reason: discord.Option(
            discord.SlashCommandOptionType.string,
            name="이유",
            description="밴하는 이유",
            required=False,
        ),  # type: ignore
    ):
        await member.ban(delete_message_days=7, reason=reason)

        await ctx.respond(
            f"{member.name}님을 {ctx.guild.name}에서 밴했습니다.", ephemeral=True
        )

    @commands.slash_command(name="킥", description="유저를 서버에서 킥합니다.")
    @commands.has_permissions(kick_members=True)
    async def kick(
        self,
        ctx: discord.ApplicationContext,
        member: discord.Option(
            discord.Member, name="맴버", description="킥할 유저", required=True
        ),  # type: ignore
        reason: discord.Option(
            discord.SlashCommandOptionType.string,
            name="이유",
            description="킥하는 이유",
            required=False,
        ),  # type: ignore
    ):
        await member.kick(reason=reason)

        await ctx.respond(
            f"{member.name}님을 {ctx.guild.name}에서 킥했습니다.", ephemeral=True
        )

    timeout = discord.SlashCommandGroup(
        name="타임아웃", description="유저에게 타임아웃을 겁니다."
    )

    @timeout.command(name="적용", description="타임아웃을 적용합니다.")
    @commands.has_permissions(moderate_members=True)
    @commands.guild_only()
    async def add_timeout(
        self,
        ctx: discord.ApplicationContext,
        member: discord.Option(discord.Member, name="맴버", description="타임아웃할 맴버", required=True),  # type: ignore
        duration: discord.Option(discord.SlashCommandOptionType.integer, name="기간", description="타임아웃할 기간(일)", min_value=1, max_value=28, required=True),  # type: ignore
        reason: discord.Option(discord.SlashCommandOptionType.string, name="이유", description="타임아웃하는 이유", required=False),  # type: ignore
    ):
        await member.timeout_for(duration=timedelta(days=duration), reason=reason)

        await ctx.respond(
            f"{member.name}님에게 {duration}일동안 타임아웃을 적용했습니다.",
            ephemeral=True,
        )

    @timeout.command(name="해제", description="타임아웃을 해제합니다.")
    @commands.has_permissions(moderate_members=True)
    @commands.guild_only()
    async def remove_timeout(
        self,
        ctx: discord.ApplicationContext,
        member: discord.Option(discord.Member, name="맴버", description="타임아웃할 맴버", required=True),  # type: ignore
    ):
        await member.timeout_for(duration=timedelta(days=0))
        await ctx.respond(f"{member.name}님의 타임아웃을 해제했습니다.", ephemeral=True)

    @commands.slash_command(
        name="슬로우모드", description="채널에 슬로우모드를 적용하거나 해제합니다."
    )
    @commands.has_permissions(manage_channels=True)
    @commands.guild_only()
    async def slowmode(self, ctx: discord.ApplicationContext, duration: discord.Option(discord.SlashCommandOptionType.integer, min_value=0, max_value=21600, name="기간", description="슬로우모드 기간(초)", required=True)):  # type: ignore
        await ctx.channel.edit(slowmode_delay=timedelta(seconds=duration).seconds)
        await ctx.respond(f"{ctx.channel.name}의 슬로우모드를 적용했습니다.")


def setup(bot: commands.Bot):
    bot.add_cog(Moderate(bot=bot))