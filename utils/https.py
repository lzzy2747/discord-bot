from typing import Optional

from aiohttp import ClientSession
from requests import get


def get_request(url: str, params: Optional[dict | None]):
    response = get(url=url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None


async def async_get(url: str, headers: Optional[dict | None]):
    async with ClientSession(headers=headers) as session:
        async with session.get(url=url) as response:
            if response.status == 200:
                data = await response.json(content_type=None)
                return data
            else:
                return None


async def async_post(url: str, headers: Optional[dict | None], data: dict):
    async with ClientSession(headers=headers) as session:
        async with session.post(url=url, data=data) as response:
            if response.status == 200:
                data = await response.json(content_type=None)
                return data
            else:
                return None
