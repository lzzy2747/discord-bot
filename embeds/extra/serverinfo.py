import discord

from tool.unix import *


async def serverinfo(interaction: discord.Interaction, guild: discord.Guild):
    member = interaction.user
    avatar = member.display_avatar

    created_at = f"<t:{to_unix(guild.created_at)}> (<t:{to_unix(guild.created_at)}:R>)"

    embed = discord.Embed()
    embed.set_author(name=guild.name)
    embed.set_footer(text=member.name, icon_url=avatar)
    embed.add_field(name="ID", value=f"``{guild.id}``", inline=False)
    embed.add_field(
        name="소유자",
        value=f"{guild.owner.mention} (``{guild.owner.id}``)",
        inline=False,
    )
    embed.add_field(name="생성일", value=created_at, inline=False)
    embed.add_field(name="맴버 수", value=f"{guild.member_count}명", inline=True)
    embed.add_field(name="채널 수", value=f"{len(guild.channels)}개", inline=True)
    embed.add_field(name="역할 수", value=f"{len(guild.roles)}개", inline=True)

    return embed
