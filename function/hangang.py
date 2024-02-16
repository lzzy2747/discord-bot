from typing import Final

from tool.api import *

URL: Final[str] = "https://api.hangang.life/"


async def hangang():
    d = await get_req(URL)
    return d["DATAs"]["DATA"]["HANGANG"]
