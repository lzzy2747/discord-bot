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


def setup(bot: commands.Bot):
    bot.add_cog(Moderate(bot=bot))
