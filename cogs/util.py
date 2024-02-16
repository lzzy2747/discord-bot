import discord
from discord import app_commands
from discord.ext import commands
from simpcalc.errors import *
from simpcalc.simpcalc import Calculate

from embeds.error import error_embed
from embeds.extra.hangang import hangang_embed
from function.dictionary import dictionary
from function.hangang import hangang
from function.translate import tse


class Util(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="번역", description="다른 언어를 번역합니다.")
    @app_commands.choices(
        target=[
            app_commands.Choice(name="한국어", value="kr"),
            app_commands.Choice(name="영어", value="en"),
            app_commands.Choice(name="일본어", value="ja"),
            app_commands.Choice(name="중국어 간체", value="zh-CN"),
            app_commands.Choice(name="중국어 번체", value="zh-TW"),
            app_commands.Choice(name="베트남어", value="vi"),
            app_commands.Choice(name="인도네시아어", value="id"),
            app_commands.Choice(name="태국어", value="th"),
            app_commands.Choice(name="독일어", value="de"),
            app_commands.Choice(name="러시아어", value="ru"),
            app_commands.Choice(name="스페인어", value="es"),
            app_commands.Choice(name="이탈리아어", value="it"),
            app_commands.Choice(name="프랑스어", value="fr"),
        ]
    )
    @app_commands.rename(target="대상언어", query="내용")
    @app_commands.describe(target="번역될 언어", query="번역할 내용")
    async def translate(
        self,
        interaction: discord.Integration,
        target: app_commands.Choice[str],
        query: str,
    ):
        r = await tse(s=query, t=target.value, q=query)

        await interaction.response.defer(thinking=True, ephemeral=True)
        await interaction.followup.send(r, ephemeral=True)

    @app_commands.command(name="사전", description="단어의 뜻을 알려줍니다.")
    @app_commands.rename(query="용어")
    @app_commands.describe(query="찾아볼 용어")
    async def dictionary(self, interaction: discord.Interaction, query: str):
        d = await dictionary(q=query)

        if d is None:
            await interaction.response.defer(thinking=True, ephemeral=True)
            return await interaction.followup.send(
                embed=await error_embed(
                    description="뜻을 찾을 수 없습니다. 올바른 용어인 지 확인해주세요."
                ),
                ephemeral=True,
            )

        i = d["channel"]["item"]

        embed = discord.Embed(description=f"📖 {query}의 사전 검색결과")

        for j in range(len(d)):
            df: str = i[j]["sense"]["definition"]
            p: str = i[j]["pos"]

            embed.add_field(
                name=f"{query}",
                value=f"「{p}」 {df}",
                inline=False,
            )

        await interaction.response.defer(thinking=True, ephemeral=False)
        await interaction.followup.send(embed=embed, ephemeral=False)

    @app_commands.command(name="한강", description="한강 수온을 불러옵니다.")
    async def hangang(self, interaction: discord.Interaction):
        d = await hangang()

        temp = d["안양천"]["TEMP"]
        ph = d["안양천"]["PH"]
        date = d["안양천"]["LAST_UPDATE"]

        await interaction.response.defer(thinking=True, ephemeral=False)
        await interaction.followup.send(
            embed=await hangang_embed(temp, date, ph), ephemeral=False
        )

    @app_commands.command(name="계산기", description="수식을 계산합니다.")
    @app_commands.rename(expression="수식")
    @app_commands.describe(expression="계산할 수식")
    async def calculate(self, interaction: discord.Interaction, expression: str):
        try:
            c = Calculate()
            r = await c.calculate(expr=expression)

            await interaction.response.defer(thinking=True, ephemeral=False)
            await interaction.followup.send(r, ephemeral=False)
        except BadArgument:
            await interaction.response.defer(thinking=True, ephemeral=True)
            await interaction.followup.send(
                embed=await error_embed(description="올바르지 않은 수식입니다."),
                ephemeral=True,
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Util(bot=bot))
