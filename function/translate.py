import os
from typing import Final

from dotenv import load_dotenv
from tool.api import *

load_dotenv(dotenv_path="../.env")

DURL: Final[str] = "https://openapi.naver.com/v1/papago/detectLangs"
NURL: Final[str] = "https://openapi.naver.com/v1/papago/n2mt"

KEY: Final[str] = os.getenv("NVR_KEY")
SEC: Final[str] = os.getenv("NVR_SEC")

h: Final[dict] = {
    "X-Naver-Client-Id": KEY,
    "X-Naver-Client-Secret": SEC,
}


async def dtt(q: str):
    p: Final[dict] = {"query": q}
    d = await post_req(DURL, h, p)

    return d["langCode"]


async def tse(s: str, t: str, q: str):
    p: Final[dict] = {"source": await dtt(q=s), "target": t, "text": q}
    d = await post_req(NURL, h, p)
    r = d["message"]["result"]["translatedText"]

    return r
