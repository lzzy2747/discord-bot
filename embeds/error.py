from typing import Optional

import discord


async def error_embed(description: Optional[str]):
    embed = discord.Embed(description=f"> ❌ {description}", color=discord.Color.red())
    return embed
