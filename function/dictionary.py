import os
from typing import Final

from dotenv import load_dotenv
from tool.api import *

load_dotenv(dotenv_path="../.env")

KEY: Final[str] = os.getenv("DICT_KEY")


async def dictionary(q: str):
    d = await get_req(
        f"https://stdict.korean.go.kr/api/search.do?certkey_no=6330&key={KEY}&type_search=search&req_type=json&q={q}",
        h=None,
    )

    # print(d['channel']['item'])
    return d
