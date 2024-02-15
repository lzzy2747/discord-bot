from os import getenv

from dotenv import load_dotenv
from utils.https import *

load_dotenv(dotenv_path="../.env")


URL: list = [
    "https://openapi.naver.com/v1/util/shorturl.json",  # 링크 단축
    "https://openapi.naver.com/v1/papago/detectLangs",  # 언어 감지
    "https://openapi.naver.com/v1/papago/n2mt",  # 번역
]
HEADERS: dict = {
    "X-Naver-Client-Id": getenv("NAVER_ID"),
    "X-Naver-Client-Secret": getenv("NAVER_SECRET"),
}


async def detect_language(query: str):
    PARAM: dict = {"query": query}
    data = await async_post(
        url=URL[1],
        data=PARAM,
        headers=HEADERS,
    )

    return data["langCode"]


async def translate(query: str, target: str, text: str):
    PARAM: dict = {
        "source": await detect_language(query=query),
        "target": target,
        "text": text,
    }
    data = await async_post(
        url=URL[2],
        data=PARAM,
        headers=HEADERS,
    )

    return data["message"]["result"]["translatedText"]


async def shorten_url(url: str):
    PARAM: dict = {"url": url}
    data = await async_post(
        url=URL[0],
        data=PARAM,
        headers=HEADERS,
    )

    return data["result"]["url"]
