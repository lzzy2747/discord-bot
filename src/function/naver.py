from os import getenv

from dotenv import load_dotenv

from function.https import post

load_dotenv(dotenv_path="../.env")

SHORTEN_API_URL: str = "https://openapi.naver.com/v1/util/shorturl.json"
HEADERS: dict = {
    "X-Naver-Client-Id": getenv("NAVER_ID"),
    "X-Naver-Client-Secret": getenv("NAVER_SECRET"),
}


async def shorten_url(url: str):
    PARAM: dict = {"url": url}
    data = await post(
        url=SHORTEN_API_URL,
        data=PARAM,
        headers=HEADERS,
    )

    return data["result"]["url"]
