from os import getenv

from dotenv import load_dotenv

from function.https import post

load_dotenv(dotenv_path="../.env")

SHORTEN_API_URL: str = "https://openapi.naver.com/v1/util/shorturl.json"
SHORTEN_URL_HEADERS: dict = {
    "X-Naver-Client-Id": getenv("ZkDhOq63Ay6TjbyZDfXO"),
    "X-Naver-Client-Secret": getenv("EKDc0LJUs6"),
}


async def shorten_url(url: str):
    PARAM: dict = {"url": url}
    data = await post(
        url=SHORTEN_API_URL,
        data=PARAM,
        headers=SHORTEN_URL_HEADERS,
    )

    return data["result"]["url"]
