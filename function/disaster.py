from os import getenv
from typing import Final

from dotenv import load_dotenv
from requests import get

load_dotenv(dotenv_path="../.env")

s = getenv(key="SERVICE_KEY")


def disaster():
    p: Final[dict] = {"serviceKey": s, "pageNo": "1", "numOfRows": "5", "type": "json"}
    res = get(
        "http://apis.data.go.kr/1741000/DisasterMsg3/getDisasterMsg1List", params=p
    )

    d = res.json()
    return d["DisasterMsg"][1]["row"]
