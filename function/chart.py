from bs4 import BeautifulSoup
from requests import get

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko"
}
URL: str = "https://www.melon.com/chart/index.htm"
IMG: str = (
    "data:image/png;base64,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"
)


def chart():
    request = get(URL, headers=HEADERS).text
    soup = BeautifulSoup(request, "html.parser")

    return soup


def get_title() -> list:
    title_list: list = []
    title = chart().find_all("div", {"class": "ellipsis rank01"})

    for i in title:
        title_list.append(i.find("a").text)

    return title_list


def get_artist() -> list:
    artist_list: list = []
    artist = chart().find_all("div", {"class": "ellipsis rank02"})

    for j in artist:
        artist_list.append(j.find("span", {"class": "checkEllipsis"}).text)

    return artist_list
