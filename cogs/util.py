import discord
from discord.ext import commands
from simpcalc.errors import BadArgument, Overflow
from simpcalc.simpcalc import Calculate
import aiohttp


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
            await ctx.respond("결과 값이 너무 큽니다.", ephemeral=True)
        except BadArgument:
            await ctx.respond(
                "잘못된 수식 입력입니다. 다시 입력해주세요.", ephemeral=True
            )

    @commands.slash_command(name="한강", description="한강 수온을 알려줍니다.")
    async def river(self, ctx: discord.ApplicationContext):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.hangang.life/') as response:
                if response.status == 200:
                    data = await response.json()
                    temp = data['DATA']["HANGANG"]["노량진"]["TEMP"]

                    await ctx.respond(f'{temp}°C')

def setup(bot: commands.Bot):
    bot.add_cog(Util(bot=bot))
