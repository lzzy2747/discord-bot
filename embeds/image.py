import discord


async def image_embed(url: str):
    embed = discord.Embed(color=discord.Color.random())
    embed.set_image(url=url)

    return embed
