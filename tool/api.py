from typing import Optional

from aiohttp import ClientSession


async def get_req(u: str, h: Optional[dict] = None):
    async with ClientSession(headers=h) as session:
        async with session.get(url=u) as response:
            if response.status == 200:
                d = await response.json(content_type=None)
                return d
            else:
                return None


async def post_req(u: str, h: Optional[dict] = None, d: Optional[dict] = None):
    async with ClientSession(headers=h) as session:
        async with session.post(url=u, data=d) as response:
            if response.status == 200:
                dr = await response.json(content_type=None)
                return dr
            else:
                return None
