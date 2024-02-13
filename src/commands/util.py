from os import getenv

import discord
from discord.ext import commands
from discord.ui import Button, View
from dotenv import load_dotenv
from inko import Inko
from simpcalc.errors import BadArgument, Overflow
from simpcalc.simpcalc import Calculate

from function.disaster import disaster_content, disaster_date
from util.https import get_async
from function.naver import CHOICE_LANG, LANG_CODE, shorten_url, translate
from function.sun import sunrise, sunset

load_dotenv(dotenv_path="../.env")


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
        ),
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

    @commands.slash_command(name="한타", description="영타를 한타로 변환합니다.")
    async def hanta(
        self,
        ctx: discord.ApplicationContext,
        query: discord.Option(
            discord.SlashCommandOptionType.string,
            name="문자",
            description="변환할 문자",
            required=True,
        ),
    ):
        inko = Inko()
        await ctx.respond(f"{inko.en2ko(query)}", ephemeral=True)

    @commands.slash_command(name="단축", description="링크를 단축합니다.")
    async def shorturl(
        self,
        ctx: discord.ApplicationContext,
        url: discord.Option(
            discord.SlashCommandOptionType.string,
            name="링크",
            description="단축할 링크",
        ),
    ):
        url = await shorten_url(url=url)

        button = Button(
            label="바로가기",
            style=discord.ButtonStyle.link,
            url=url,
            emoji="🔗",
        )
        view = View()
        view.add_item(button)

        await ctx.response.send_message("단축이 되었습니다.", view=view, ephemeral=True)

    @commands.slash_command(
        name="재난문자", description="최근 발송된 재난문자를 불러옵니다."
    )
    async def disaster(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(description=disaster_content())
        embed.set_footer(text=disaster_date())
        await ctx.respond(embed=embed)

    @commands.slash_command(name="강아지", description="강아지 사진을 가져옵니다.")
    async def dog(self, ctx: discord.ApplicationContext):
        data = await get_async(
            url="https://dog.ceo/api/breeds/image/random", headers=None
        )
        img = data["message"]

        embed = discord.Embed()
        embed.set_image(url=img)
        await ctx.respond(embed=embed)

    @commands.slash_command(name="사전", description="사전을 검색합니다.")
    async def dictionary(
        self,
        ctx: discord.ApplicationContext,
        query: discord.Option(
            discord.SlashCommandOptionType.string,
            name="검색어",
            description="검색할 단어",
            required=True,
        ),
    ):
        URL: str = (
            f"https://stdict.korean.go.kr/api/search.do?certkey_no=6330&key={getenv('DICTIONARY_API_KEY')}&type_search=search&req_type=json&q={query}"
        )
        data = await get_async(url=URL, headers=None)

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
            await ctx.respond(embed=embed)
        else:
            await ctx.respond("검색 결과를 찾을 수 없습니다.", ephemeral=True)

    @commands.slash_command(name="고양이", description="고양이 사진을 가져옵니다.")
    async def cat(self, ctx: discord.ApplicationContext):
        data = await get_async(
            "https://api.thecatapi.com/v1/images/search?limit=1", headers=None
        )
        img = data[0]["url"]

        embed = discord.Embed()
        embed.set_image(url=img)
        await ctx.respond(embed=embed)

    @commands.slash_command(name="한강", description="한강 수온을 알려줍니다.")
    async def river(self, ctx: discord.ApplicationContext):
        data = await get_async(url="https://api.hangang.life/", headers=None)
        temp = data["DATAs"]["DATA"]["HANGANG"]["노량진"]["TEMP"]
        await ctx.respond(f"{temp}°C")

    @commands.slash_command(name="출몰시간", description="출몰 시간을 알려줍니다.")
    async def suntime(self, ctx: discord.ApplicationContext):
        embed = discord.Embed()
        embed.add_field(
            name="☀️ 일출",
            value=f"{int(sunrise()[:2])}시 {int(sunrise()[2:])}분",
            inline=False,
        )
        embed.add_field(
            name="🌙 일몰",
            value=f"{int(sunset()[:2])}시 {int(sunset()[2:])}분",
            inline=False,
        )
        await ctx.respond(embed=embed)

    @commands.slash_command(name="번역", description="언어를 번역해줍니다.")
    async def trans(
        self,
        ctx: discord.ApplicationContext,
        target: discord.Option(
            discord.SlashCommandOptionType.string,
            name="대상언어",
            description="번역할 대상이 될 언어",
            choices=CHOICE_LANG,
            required=True,
        ),
        text: discord.Option(
            discord.SlashCommandOptionType.string,
            name="내용",
            description="번역될 내용",
            required=True,
        ),
    ):
        data = await translate(query=text, target=LANG_CODE[target], text=text)
        await ctx.respond(f"{data}", ephemeral=False)


def setup(bot: commands.Bot):
    bot.add_cog(Util(bot=bot))
