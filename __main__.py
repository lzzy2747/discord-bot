from logging import INFO, basicConfig
from os import getenv, listdir

from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv


class Main(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(help_commands=None, intents=Intents.all())
        basicConfig(level=INFO)
        load_dotenv(dotenv_path="./.env")

    async def on_ready(self):
        print(f"Logged as {self.user.name}")
        print(f"Loaded {len(self.extensions)} extensions")

    def run(self):
        super().run(getenv(key="BOT_TOKEN"))


bot = Main()

if __name__ == "__main__":
    for filename in listdir("./cogs"):
        if filename.endswith(".py") and not filename.startswith("__"):
            bot.load_extension(f"cogs.{filename[:-3]}")

    bot.run()
