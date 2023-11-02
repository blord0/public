import discord

bot = discord.Client(intents=discord.Intents.messages)

@bot.event
async def on_ready():
    print(f"Hooked into {bot.user}")

@bot.event
async def on_message(message: discord.Message):
    
    if message.author.id == bot.user.id: # Stops if last message was us
        return

    if message.guild.id != 1035115107178512384: # Only reply in this guild
        return

    if "poor" in message.content.lower():
        print("Someone said poor | " + str(message.author) + ": " + message.content)
        await message.channel.send("You are poor lol", reference=message)

bot.run(token)
