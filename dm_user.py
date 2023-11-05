import discord
import os

dm_user=int(input("Input recipient user id:\n"))
dm_content=input("Input what message you want to send to them:\n")

bot = discord.Client(intents=discord.Intents.default())

@bot.event
async def on_ready():
  user=bot.get_user(dm_user)
  dm = await user.create_dm()
  await dm.send(dm_content)
  print(f"Sent message to {user}")
  print(f"Sent '{dm_content}'")
  os.kill(os.getpid(), 9)

bot.run(token)
