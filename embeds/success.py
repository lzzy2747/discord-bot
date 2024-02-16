from typing import Optional

import discord


async def success_embed(description: Optional[str]):
    embed = discord.Embed(
        description=f"> ✅ {description}", color=discord.Color.green()
    )
    return embed
