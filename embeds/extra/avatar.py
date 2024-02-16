import discord


async def avatar(member: discord.Member):
    avatar = member.display_avatar

    embed = discord.Embed()
    embed.set_author(name=member.name)
    embed.set_image(url=avatar)

    return embed
