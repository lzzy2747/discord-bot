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
    @commands.has_permissions(manage_members=True)
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
    @commands.has_permissions(manage_members=True)
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


def setup(bot: commands.Bot):
    bot.add_cog(Moderate(bot=bot))