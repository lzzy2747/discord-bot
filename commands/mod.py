from datetime import timedelta

import discord
from discord import app_commands
from discord.ext import commands


class Mod(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_command_error(
        self, _: discord.Interaction, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingPermissions) or isinstance(
            error, commands.BotMissingPermissions
        ):
            return

        raise error

    @app_commands.command(
        name="청소", description="입력된 개수만큼 메시지를 제거합니다."
    )
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.describe(amount="개수")
    @app_commands.rename(amount="개수")
    @app_commands.guild_only()
    async def clear(self, interaction: discord.Interaction, amount: int):
        if 0 >= amount <= 100:
            await interaction.response.send_message(
                f"1건 이상 100건 이하로 입력해주세요.", ephemeral=True
            )
        else:
            await interaction.response.defer(thinking=False)
            await interaction.channel.purge(limit=amount)

    @app_commands.command(
        name="타임아웃", description="유저에게 타임아웃을 걸거나 해제합니다."
    )
    @app_commands.describe(member="맴버", duration="기간 (일)", reason="이유")
    @app_commands.rename(member="맴버", duration="기간", reason="이유")
    @app_commands.checks.has_permissions(moderate_members=True)
    @app_commands.guild_only()
    async def timeout(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        duration: int,
        reason: str = None,
    ):
        if 0 < duration < 28:
            return await interaction.response.send_message(
                f"0일에서 28일 사이로 타임아웃을 걸 수 있습니다.", ephemeral=True
            )

        if duration != 0:
            if member.is_timed_out:
                return await interaction.response.send_message(
                    f"{member.mention}님은 이미 타임아웃 상태입니다."
                )

            await member.timeout(timedelta(days=duration), reason=reason)
            await interaction.response.send_message(
                f"{member.mention}님에게 {duration}일동안 타임아웃을 적용했습니다."
            )
        else:
            if not member.is_timed_out:
                return await interaction.response.send_message(
                    f"{member.mention}님은 이미 타임아웃 해제 상태입니다."
                )

            await member.timeout(None, reason=reason)
            await interaction.response.send_message(
                f"{member.mention}님에 타임아웃을 해제했습니다.", ephemeral=True
            )

    @app_commands.command(name="킥", description="유저를 킥합니다.")
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.describe(member="맴버", reason="이유")
    @app_commands.rename(member="맴버", reason="이유")
    @app_commands.guild_only()
    async def kick(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = None,
    ):
        if member.id == interaction.user.id:
            return

        await member.kick(reason=reason)
        await interaction.response.send_message(f"{member.mention}님을 킥했습니다.")

    @app_commands.command(name="밴", description="유저를 밴합니다.")
    @app_commands.choices(
        duration=[
            app_commands.Choice(name="1일", value=1),
            app_commands.Choice(name="2일", value=2),
            app_commands.Choice(name="3일", value=3),
            app_commands.Choice(name="4일", value=4),
            app_commands.Choice(name="5일", value=5),
            app_commands.Choice(name="6일", value=6),
            app_commands.Choice(name="7일", value=7),
        ]
    )
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.guild_only()
    @app_commands.describe(member="맴버", reason="이유", duration="기간")
    @app_commands.rename(member="맴버", duration="기간", reason="이유")
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = None,
        *,
        duration: app_commands.Choice[int] = None,
    ):
        if member.id == interaction.user.id:
            return

        if duration is None:
            return await member.ban(reason=reason)

        await member.ban(delete_message_days=duration.value, reason=reason)
        await interaction.response.send_message(f"{member.mention}님을 밴했습니다.")

    @app_commands.command(name="역할", description="유저의 역할을 관리합니다.")
    @app_commands.guild_only()
    @app_commands.choices(
        decision=[
            app_commands.Choice(name="추가", value=1),
            app_commands.Choice(name="제거", value=2),
        ]
    )
    @app_commands.describe(member="맴버", role="역할", decision="여부")
    @app_commands.rename(member="맴버", role="역할", decision="여부")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def roles(
        self,
        interaction: discord.Interaction,
        decision: app_commands.Choice[int],
        member: discord.Member,
        role: discord.Role,
    ):
        if decision.value == 1:
            await member.add_roles(role)
            await interaction.response.send_message(
                f"{member.mention}님에게 {role.mention}을 {decision.name}했습니다.",
                ephemeral=False,
            )
        else:
            await member.remove_roles(role)
            await interaction.response.send_message(
                f"{member.mention}님에게 {role.mention}을 {decision.name}했습니다.",
                ephemeral=False,
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Mod(bot=bot))
