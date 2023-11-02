# Reset all "/" commands for the bot
import discord
import time
import os

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        print("Starting...")

bot = MyClient()

@bot.event
async def on_ready():
    print(f"Hooked into {bot.user}")
    time.sleep(2)
    print("Done!")
    os.kill(os.getpid(), 9)

bot.run(token)
