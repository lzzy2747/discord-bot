from os import getenv

from dotenv import load_dotenv

from function.https import post

load_dotenv(dotenv_path="../.env")

LANG_CODE: dict = {  # 언어 코드
    "한국어": "ko",
    "영어": "en",
    "일본어": "jp",
    "중국어 간체": "zh-CN",
    "중국어 번체": "zh-TW",
    "베트남어": "vi",
    "인도네시아어": "id",
    "태국어": "th",
    "독일어": "de",
    "러시아어": "ru",
    "스페인어": "es",
    "이탈리아어": "it",
    "프랑스어": "fr",
}

CHOICE_LANG: list = [  # 지원 언어 목록
    "한국어",
    "영어",
    "일본어",
    "중국어 간체",
    "중국어 번체",
    "베트남어",
    "인도네시아어",
    "태국어",
    "독일어",
    "러시아어",
    "스페인어",
    "이탈리아어",
    "프랑스어",
]

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
    data = await post(
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
