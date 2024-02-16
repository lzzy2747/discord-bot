from typing import Final

from bs4 import BeautifulSoup as bs
from requests import get

h: Final[dict] = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
}


def melon():
    res = get(url="https://www.melon.com/chart/", headers=h).text
    soup = bs(res, "html.parser")

    return soup


def title() -> list:
    t: Final[list] = []
    tl = melon().find_all("div", {"class": "ellipsis rank01"})

    for i in tl:
        t.append(i.find("a").text)

    return t


def singer() -> list:
    s: Final[list] = []
    sg = melon().find_all("div", {"class": "ellipsis rank02"})

    for j in sg:
        s.append(j.find("span", {"class": "checkEllipsis"}).text)

    return s
