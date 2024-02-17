from typing import Final

from bs4 import BeautifulSoup as bs
from requests import get

h: Final[dict] = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
}
img: Final[str] = (
    "https://is1-ssl.mzstatic.com/image/thumb/Purple116/v4/e4/7f/26/e47f262f-5235-b07a-db72-1d115e1b1d22/AppIcon-1x_U007emarketing-5-0-85-220.png/512x512bb.jpg"
)


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
