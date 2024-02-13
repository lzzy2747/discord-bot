from datetime import datetime

import aiohttp
import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import commands
from discord.ui import Button, View
from simpcalc.errors import BadArgument, Overflow
from simpcalc.simpcalc import Calculate

from etc.config import serviceKey, shorten_url_key, shorten_url_pw


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

    @commands.slash_command(name="단축", description="링크를 단축합니다.")
    async def shorturl(
        self,
        ctx: discord.ApplicationContext,
        url: discord.Option(
            discord.SlashCommandOptionType.string,
            name="링크",
            description="단축할 링크",
        ),  # type: ignore
    ):
        headers: dict = {
            "X-Naver-Client-Id": shorten_url_key,
            "X-Naver-Client-Secret": shorten_url_pw,
        }
        params: dict = {"url": url}

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(
                "https://openapi.naver.com/v1/util/shorturl.json", data=params
            ) as response:
                if response.status == 200:
                    data = await response.json()

                    url = data["result"]["url"]

                    button = Button(
                        label="바로가기",
                        style=discord.ButtonStyle.link,
                        url=url,
                        emoji="🔗",
                    )
                    view = View()
                    view.add_item(button)

                    await ctx.response.send_message(
                        "단축이 되었습니다.", view=view, ephemeral=True
                    )

    @commands.slash_command(
        name="재난문자", description="최근 발송된 재난문자를 불러옵니다."
    )
    async def disaster(self, ctx: discord.ApplicationContext):
        params = {
            "serviceKey": serviceKey,
            "pageNo": "1",
            "numOfRows": "1",
            "type": "json",
        }
        response = requests.get(
            "http://apis.data.go.kr/1741000/DisasterMsg3/getDisasterMsg1List",
            params=params,
        )

        data = response.json()

        time = data["DisasterMsg"][1]["row"][0]["create_date"]
        msg = data["DisasterMsg"][1]["row"][0]["msg"]

        embed = discord.Embed(description=msg)
        embed.set_footer(text=time)
        await ctx.respond(embed=embed)

    @commands.slash_command(name="강아지", description="강아지 사진을 가져옵니다.")
    async def dog(self, ctx: discord.ApplicationContext):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://dog.ceo/api/breeds/image/random"
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    img = data["message"]

                    embed = discord.Embed()
                    embed.set_image(url=img)
                    await ctx.respond(embed=embed)

    @commands.slash_command(name="고양이", description="고양이 사진을 가져옵니다.")
    async def cat(self, ctx: discord.ApplicationContext):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.thecatapi.com/v1/images/search?limit=1"
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    img = data[0]["url"]

                    embed = discord.Embed()
                    embed.set_image(url=img)
                    await ctx.respond(embed=embed)

    @commands.slash_command(name="한강", description="한강 수온을 알려줍니다.")
    async def river(self, ctx: discord.ApplicationContext):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.hangang.life/") as response:
                if response.status == 200:
                    data = await response.json()
                    temp = data["DATAs"]["DATA"]["HANGANG"]["노량진"]["TEMP"]

                    await ctx.respond(f"{temp}°C")

    @commands.slash_command(name="출몰시간", description="출몰 시간을 알려줍니다.")
    async def sun_time(self, ctx: discord.ApplicationContext):
        url = "http://apis.data.go.kr/B090041/openapi/service/RiseSetInfoService/getAreaRiseSetInfo"
        params = {
            "serviceKey": serviceKey,
            "locdate": datetime.now().strftime("%Y%m%d"),
            "location": "서울",
        }
        response = requests.get(url, params=params)

        content = response.text

        xml_object = BeautifulSoup(content, "lxml-xml")
        sunrise = (
            xml_object.find("body").find("items").find("item").find("sunrise").text
        )
        sunset = xml_object.find("body").find("items").find("item").find("sunset").text

        embed = discord.Embed()
        embed.add_field(
            name="☀️ 일출",
            value=f"{int(sunrise[:2])}시 {int(sunrise[2:])}분",
            inline=False,
        )
        embed.add_field(
            name="🌙 일몰",
            value=f"{int(sunset[:2])}시 {int(sunset[2:])}분",
            inline=False,
        )
        await ctx.respond(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Util(bot=bot))
