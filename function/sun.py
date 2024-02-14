from datetime import datetime
from os import getenv

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from requests import get

load_dotenv(dotenv_path="../.env")

LOCATION: str = "서울"
TIME_FORMAT: str = "%Y%m%d"
URL: str = (
    "http://apis.data.go.kr/B090041/openapi/service/RiseSetInfoService/getAreaRiseSetInfo"
)

locdate = datetime.now().strftime(TIME_FORMAT)
PARAMS: dict = {
    "serviceKey": getenv("SERVICE_URL"),
    "locdate": locdate,
    "location": LOCATION,
}


def sunrise():
    content = get(url=URL, params=PARAMS).text
    soup = BeautifulSoup(content, "lxml-xml")

    return soup.find("body").find("items").find("item").find("sunrise").text


def sunset():
    content = get(url=URL, params=PARAMS).text
    soup = BeautifulSoup(content, "lxml-xml")

    return soup.find("body").find("items").find("item").find("sunset").text
