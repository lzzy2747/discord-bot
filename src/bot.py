from os import getenv, listdir

from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv


class Bot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(help_commands=None, intents=Intents.all())

        load_dotenv(dotenv_path="../.env")

    async def on_ready(self):
        print(f"Logged as {self.user.name}")
        print(f"Loaded {len(bot.extensions)} extensions")

    def run(self):
        return super().run(getenv(key="BOT_TOKEN"))


bot = Bot()

if __name__ == "__main__":
    for filename in listdir("./commands"):
        if filename.endswith(".py") and not filename.startswith("__"):
            bot.load_extension(f"commands.{filename[:-3]}")

    bot.run()
