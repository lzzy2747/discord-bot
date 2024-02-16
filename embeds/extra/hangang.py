import discord


async def hangang_embed(temp: int, date: str, ph: int):
    embed = discord.Embed()

    embed.add_field(name="🌡️ 온도", value=f"{temp}℃", inline=True)
    embed.add_field(name="🧪 산성도", value=ph, inline=True)
    embed.set_footer(text=date)

    return embed
