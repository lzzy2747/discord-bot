from os import getenv, listdir

import discord
from discord.ext import commands
from dotenv import load_dotenv


class Main(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix="/",
            help_command=None,
            intents=discord.Intents.all(),
            allow_mentions=discord.AllowedMentions(
                everyone=False, users=False, roles=False, replied_user=False
            ),
        )

        load_dotenv()

    async def on_ready(self):
        synced = await self.tree.sync()
        print(f"Synced {len(synced)} commands")

        print(f"Logged as in {self.user.id}")

    async def setup_hook(self):
        for filename in listdir("./commands"):
            if filename.endswith(".py") and not filename.startswith("__"):
                await self.load_extension(f"commands.{filename[:-3]}")

    def run(self):
        return super().run(token=getenv(key="BOT_TOKEN"), reconnect=True)


bot = Main()

if __name__ == "__main__":
    bot.run()
