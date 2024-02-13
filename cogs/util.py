import discord
from discord.ext import commands
from simpcalc.errors import BadArgument, Overflow
from simpcalc.simpcalc import Calculate


class Util(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="계산", description="입력한 수식을 계산합니다.")
    async def calculator(
        self,
        ctx: discord.ApplicationContext,
        expression: discord.Option(
            discord.SlashCommandOptionType.string,
            name="수식",
            description="계산할 수식",
            required=True,
        ),  # type: ignore
    ):
        try:
            result = await Calculate().calculate(expr=expression)
            await ctx.respond(result)
        except Overflow:
            await ctx.respond(
                "결과 값이 너무 큽니다.", ephemeral=True, delete_after=5.0
            )
        except BadArgument:
            await ctx.respond(
                "잘못된 수식 입력입니다. 다시 입력해주세요.",
                ephemeral=True,
                delete_after=5.0,
            )


def setup(bot: commands.Bot):
    bot.add_cog(Util(bot=bot))
