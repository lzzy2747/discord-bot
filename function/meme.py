from utils.https import async_get


async def meme(category: str):
    data = await async_get(url=f"https://api.waifu.pics/sfw/{category}")
    return data["url"]
