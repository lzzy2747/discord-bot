from tool.api import *


async def dog():
    d = await get_req("https://dog.ceo/api/breeds/image/random", None)
    r = d["message"]

    return r


async def cat():
    d = await get_req("https://api.thecatapi.com/v1/images/search?limit=1", None)
    r = d[0]["url"]

    return r


async def waifu(category: str):
    d = await get_req(f"https://api.waifu.pics/sfw/{category}", None)
    r = d["url"]

    return r
