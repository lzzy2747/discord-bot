from utils.https import async_get

URL: str = "https://meme-api.com/gimmes"


async def meme():
    data = await async_get(url=URL, headers=None)
    return data
