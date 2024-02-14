from os import getenv

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from inko import Inko
from simpcalc.errors import *
from simpcalc.simpcalc import Calculate

from function.disaster import disaster_content, disaster_date
from function.meme import meme
from function.naver import shorten_url, translate
from function.sun import sunrise, sunset
from utils.https import *

load_dotenv(dotenv_path=".env")


class Util(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="계산", description="입력한 수식을 계산합니다.")
    @app_commands.rename(expression="수식")
    @app_commands.describe(expression="수식")
    async def calculator(self, interaction: discord.Interaction, expression: str):
        try:
            result = await Calculate().calculate(expr=expression)
            await interaction.response.send_message(result)
        except Overflow:
            await interaction.response.send_message(
                "결과 값이 너무 큽니다.", ephemeral=True
            )
        except BadArgument:
            await interaction.response.send_message(
                "잘못된 수식 입력입니다. 다시 입력해주세요.", ephemeral=True
            )

    @app_commands.command(name="짤", description="짤을 보내줍니다.")
    @app_commands.choices(
        category=[
            app_commands.Choice(name="와이프", value="waifu"),
            app_commands.Choice(name="네코", value="neko"),
            app_commands.Choice(name="시노부", value="shinobu"),
            app_commands.Choice(name="메구밍", value="megumin"),
            app_commands.Choice(name="안기", value="hug"),
            app_commands.Choice(name="울기", value="cry"),
            app_commands.Choice(name="키스", value="kiss"),
            app_commands.Choice(name="흔들기", value="wave"),
            app_commands.Choice(name="하이파이브", value="highfive"),
        ]
    )
    @app_commands.describe(category="목록")
    @app_commands.rename(category="목록")
    async def memes(
        self, interaction: discord.Interaction, category: app_commands.Choice[str]
    ):
        data = await meme(category=category.value)

        embed = discord.Embed()
        embed.set_image(url=data)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="한타", description="영타를 한타로 변환합니다.")
    @app_commands.rename(content="문자")
    @app_commands.describe(content="변환할 문자")
    async def hanta(self, interaction: discord.Interaction, content: str):
        inko = Inko()
        await interaction.response.send_message(
            f"{inko.en2ko(content)}", ephemeral=True
        )

    @app_commands.command(name="단축", description="링크를 단축합니다.")
    @app_commands.describe(url="단축할 링크")
    @app_commands.rename(url="링크")
    async def shorten_url(self, interaction: discord.Interaction, url: str):
        url = await shorten_url(url=url)

        button = discord.Button(
            label="바로가기",
            style=discord.ButtonStyle.link,
            url=url,
            emoji="🔗",
        )
        view = discord.View()
        view.add_item(button)

        await interaction.response.send_message(
            "단축이 되었습니다.", view=view, ephemeral=True
        )

    @app_commands.command(name="사전", description="사전을 검색합니다.")
    @app_commands.describe(query="검색어")
    @app_commands.rename(query="검색어")
    async def dictionary(self, interaction: discord.Interaction, query: str):
        URL: str = (
            f"https://stdict.korean.go.kr/api/search.do?certkey_no=6330&key={getenv('DICTIONARY_API_KEY')}&type_search=search&req_type=json&q={query}"
        )
        data = await async_get(url=URL, headers=None)

        if data:
            items = data["channel"]["item"]

            embed = discord.Embed(description=f"{query}의 대한 검색어")
            for i in range(0, len(items)):
                define = items[i]["sense"]["definition"]
                pos = items[i]["pos"]

                embed.add_field(
                    name=f"{query}",
                    value=f"「{pos}」 {define}",
                    inline=False,
                )
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(
                "검색 결과를 찾을 수 없습니다.", ephemeral=True
            )

    @app_commands.command(
        name="재난문자", description="최근 발송된 재난문자를 불러옵니다."
    )
    async def disaster_message(self, interaction: discord.Interaction):
        embed = discord.Embed(description=disaster_content())
        embed.set_footer(text=disaster_date())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="한강", description="한강 수온을 알려줍니다.")
    async def river(self, interaction: discord.Interaction):
        data = await async_get(url="https://api.hangang.life/", headers=None)
        temp = data["DATAs"]["DATA"]["HANGANG"]["노량진"]["TEMP"]
        await interaction.response.send_message(f"{temp}°C")

    @app_commands.command(name="강아지", description="강아지 사진을 가져옵니다.")
    async def dog(self, interaction: discord.Interaction):
        data = await async_get(
            url="https://dog.ceo/api/breeds/image/random", headers=None
        )
        img = data["message"]

        embed = discord.Embed()
        embed.set_image(url=img)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="고양이", description="고양이 사진을 가져옵니다.")
    async def cat(self, interaction: discord.Interaction):
        data = await async_get(
            "https://api.thecatapi.com/v1/images/search?limit=1", headers=None
        )
        img = data[0]["url"]

        embed = discord.Embed()
        embed.set_image(url=img)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="출몰시간", description="출몰 시간을 알려줍니다.")
    async def suntime(self, interaction: discord.Interaction):
        embed = discord.Embed()
        embed.add_field(
            name="🌅 일출",
            value=f"{int(sunrise()[:2])}시 {int(sunrise()[2:])}분",
            inline=False,
        )
        embed.add_field(
            name="🌃 일몰",
            value=f"{int(sunset()[:2])}시 {int(sunset()[2:])}분",
            inline=False,
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="번역", description="언어를 번역해줍니다.")
    @app_commands.describe(query="번역할 내용", target="대상 언어")
    @app_commands.rename(query="내용", target="대상언어")
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
    async def trans(
        self,
        interaction: discord.Interaction,
        query: str,
        target: app_commands.Choice[str],
    ):
        data = await translate(query=query, target=target.value, text=query)
        await interaction.response.send_message(f"{data}", ephemeral=False)


async def setup(bot: commands.Bot):
    await bot.add_cog(Util(bot=bot))
