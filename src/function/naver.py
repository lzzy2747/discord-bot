from os import getenv

from dotenv import load_dotenv

from function.https import post

load_dotenv(dotenv_path="../.env")

LANG: dict = {
    "ko": "한국어",
    "en": "영어",
    "ja": "일본어",
    "zh-CN": "중국어 간체",
    "zh-TW": "중국어 번체",
    "vi": "베트남어",
    "id": "인도네시아어",
    "th": "태국어",
    "de": "독일어",
    "ru": "러시아어",
    "es": "스페인어",
    "it": "이탈리아어",
    "fr": "프랑스어",
}

URL: list = [
    "https://openapi.naver.com/v1/util/shorturl.json", # 링크 단축
    "https://openapi.naver.com/v1/papago/detectLangs", # 언어 감지
    "https://openapi.naver.com/v1/papago/n2mt", # 번역
]
HEADERS: dict = {
    "X-Naver-Client-Id": getenv("NAVER_ID"),
    "X-Naver-Client-Secret": getenv("NAVER_SECRET"),
}


async def detect_language(query: str):
    PARAM: dict = {"query": query}
    data = await post(
        url=URL[1],
        data=PARAM,
        headers=HEADERS,
    )

    return data["langCode"]


async def translate(src: str, target: str, text: str):
    PARAM: dict = {"source": detect_language(query=src), "target": target, "text": text}
    data = await post(
        url=URL[2],
        data=PARAM,
        headers=HEADERS,
    )

    return data["message"]["result"]["translatedText"]


async def shorten_url(url: str):
    PARAM: dict = {"url": url}
    data = await post(
        url=URL[0],
        data=PARAM,
        headers=HEADERS,
    )

    return data["result"]["url"]
