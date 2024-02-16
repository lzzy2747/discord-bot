from time import mktime

import discord


async def userinfo(member: discord.Member):
    avatar = member.display_avatar
    created_at = f"<t:{round(mktime(member.created_at.timetuple()))}> (<t:{round(mktime(member.created_at.timetuple()))}:R>)"
    joined_at = f"<t:{round(mktime(member.joined_at.timetuple()))}> (<t:{round(mktime(member.joined_at.timetuple()))}:R>)"

    status: dict = {
        discord.Status.online: "온라인",
        discord.Status.idle: "자리비움",
        discord.Status.dnd: "방해 금지",
        discord.Status.offline: "오프라인",
    }
    member_status = status[member.status]

    embed = discord.Embed()
    embed.set_author(name=member.name, icon_url=avatar)
    embed.set_footer(text=member.name, icon_url=avatar)
    embed.add_field(name="ID", value=f"``{member.id}``", inline=False)
    embed.add_field(name="언급", value=member.mention, inline=False)
    embed.add_field(name="생성일", value=created_at, inline=False)
    embed.add_field(name="가입일", value=joined_at, inline=False)
    embed.add_field(name="상태", value=member_status, inline=False)

    return embed
