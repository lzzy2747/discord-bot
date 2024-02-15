from bs4 import BeautifulSoup
from requests import get

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko"
}
URL: str = "https://www.melon.com/chart/index.htm"


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
