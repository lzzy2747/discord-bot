from datetime import timedelta

import discord
from discord import app_commands
from discord.ext import commands

from embeds.error import error_embed
from embeds.success import success_embed


class Mod(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_app_command_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ) -> None:
        if isinstance(error, commands.MissingPermissions) or isinstance(
            error, commands.BotMissingPermissions
        ):
            await interaction.response.defer(thinking=True, ephemeral=True)
            await interaction.followup.send(
                embed=await error_embed(description="권한이 부족합니다."),
                ephemeral=True,
            )

        raise error

    @app_commands.command(name="청소", description="메시지를 청소합니다.")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.rename(amount="개수")
    @app_commands.describe(amount="청소할 개수")
    async def clear(self, interaction: discord.Interaction, amount: int):
        if not 1 < amount < 100:
            await interaction.response.defer(thinking=True, ephemeral=True)
            return await interaction.followup.send(
                embed=await error_embed(
                    description="1개 이상 100개 이하에 메시지만 지울 수 있습니다."
                ),
                ephemeral=True,
            )

        await interaction.response.defer(thinking=True, ephemeral=False)
        await interaction.channel.purge(limit=amount)
        await interaction.channel.send(
            embed=await success_embed(description=f"{amount}건에 메시지를 지웠습니다."),
            delete_after=5.0,
        )

    @app_commands.command(name="슬로우모드", description="슬로우모드를 걸어줍니다.")
    @app_commands.rename(channel="채널", duration="기간")
    @app_commands.describe(channel="채널", duration="기간 (초)")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def slowmode(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel = None,
        *,
        duration: int,
    ):
        if channel is None:
            channel = interaction.channel

        if duration == 0:
            await interaction.response.defer(thinking=True, ephemeral=False)
            await interaction.channel.edit(slowmode_delay=None)
            return await interaction.followup.send(
                embed=await success_embed(
                    description=f"{channel.mention}에 슬로우모드를 해제했습니다."
                ),
                ephemeral=False,
            )

        if duration < 21600:
            await interaction.response.defer(thinking=True, ephemeral=True)
            return await interaction.followup.send(
                embed=await error_embed(description="21600초 미만으로 입력하세요."),
                ephemeral=True,
            )

        await interaction.response.defer(thinking=True, ephemeral=False)
        await interaction.channel.edit(slowmode_delay=duration)
        await interaction.followup.send(
            embed=await success_embed(
                description=f"{channel.mention}에 {duration}초에 슬로우모드를 적용했습니다."
            ),
            ephemeral=False,
        )

    @app_commands.command(name="킥", description="맴버를 킥합니다.")
    @app_commands.rename(member="맴버", reason="사유")
    @app_commands.describe(member="킥할 맴버", reason="킥하는 사유")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = None,
    ):
        if member.id == interaction.user.id:
            await interaction.response.defer(thinking=True, ephemeral=True)
            return await interaction.followup.send(
                embed=await error_embed(description="본인을 킥할 수 없습니다."),
                ephemeral=True,
            )

        await interaction.response.defer(thinking=True, ephemeral=False)
        await member.kick(reason=reason)
        await interaction.followup.send(
            embed=await success_embed(
                description=f"{member.mention}을 서버에서 킥했습니다."
            ),
            ephemeral=False,
        )

    @app_commands.command(name="밴", description="맴버를 밴합니다.")
    @app_commands.rename(member="맴버", reason="사유")
    @app_commands.describe(member="밴할 맴버", reason="밴하는 사유")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = None,
    ):
        if member.id == interaction.user.id:
            await interaction.response.defer(thinking=True, ephemeral=True)
            return await interaction.followup.send(
                embed=await error_embed(description="본인을 밴할 수 없습니다."),
                ephemeral=True,
            )

        await interaction.response.defer(thinking=True, ephemeral=False)
        await member.ban(delete_message_days=7, reason=reason)
        await interaction.followup.send(
            embed=await success_embed(
                description=f"{member.mention}을 서버에서 밴했습니다."
            ),
            ephemeral=False,
        )

    @app_commands.command(name="타임아웃", description="유저를 타임아웃합니다.")
    @app_commands.rename(member="맴버", duration="기간")
    @app_commands.describe(member="타임아웃할 맴버", duration="타임아웃하는 사유")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def timeout(
        self, interaction: discord.Interaction, member: discord.Member, duration: str
    ):
        if member.id == interaction.user.id:
            await interaction.response.defer(thinking=True, ephemeral=True)
            return await interaction.followup.send(
                embed=await error_embed(description="본인을 타임아웃할 수 없습니다."),
                ephemeral=True,
            )

        if duration == 0:
            await interaction.response.defer(thinking=True, ephemeral=True)
            return await interaction.followup.send(
                embed=await error_embed(
                    description=f"{member.mention}님의 타임아웃을 해제했습니다."
                ),
                ephemeral=True,
            )

        await interaction.response.defer(thinking=True, ephemeral=False)
        await member.timeout(until=timedelta(days=duration))
        await interaction.followup.send(
            embed=await success_embed(
                description=f"{member.mention}님의 타임아웃을 적용했습니다."
            ),
            ephemeral=False,
        )

    @app_commands.command(
        name="역할", description="유저의 역할을 추가하거나 제거합니다."
    )
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.choices(
        choose=[
            app_commands.Choice(name="추가", value=1),
            app_commands.Choice(name="제거", value=2),
        ]
    )
    @app_commands.rename(member="맴버", role="역할", choose="여부")
    @app_commands.describe(
        member="맴버", role="역할", choose="추가할 지 제거할 지 여부"
    )
    async def roles(
        self,
        interaction: discord.Interaction,
        choose: app_commands.Choice[int],
        member: discord.Member = None,
        *,
        role: discord.Role,
    ):
        if "@everyone" or "@here" in role.name:
            await interaction.response.defer(thinking=True, ephemeral=True)
            return await interaction.followup.send(
                embed=await error_embed(
                    description=f"{choose.name}할 수 없는 역할입니다."
                ),
                ephemeral=True,
            )

        if choose.value == 1:
            await interaction.response.defer(thinking=True, ephemeral=False)
            await member.add_roles(role)
            await interaction.followup.send(
                embed=await success_embed(
                    description=f"{member.mention}님에게 {role.mention}를 {choose.name}했습니다."
                ),
                ephemeral=False,
            )
        else:
            await interaction.response.defer(thinking=True, ephemeral=False)
            await member.remove_roles(role)
            await interaction.followup.send(
                embed=await success_embed(
                    description=f"{member.mention}님에게서 {role.mention}를 {choose.name}했습니다."
                ),
                ephemeral=False,
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Mod(bot=bot))
