import discord
bot = discord.Client(intents=discord.Intents(messages=True))

@bot.event
async def on_ready():
  print(f"{bot.user} is online")
  print("Current jobs: Auto react")

@bot.event
async def on_message(message: discord.Message): # Sorted mostly by importance
  react = False
  if message.author.id in [1125525137689694368,549207190330671107]: # Diavolo and Violent
    guild = await bot.fetch_guild(725466554065748088)
    emoji = await guild.fetch_emoji(1165776586889502861) # Thug shaker
    react = True

  elif message.author.id == 667276333294026772: # BLord
    guild = await bot.fetch_guild(1035115107178512384)
    emoji = await guild.fetch_emoji(1164255035174178896) # Lightsaber pepe
    react = True

  elif message.author.id == 1111505015308304384: # Jayden
    guild = await bot.fetch_guild(1035115107178512384)
    emoji = await guild.fetch_emoji(1164256858211635331) # lmao my ass off
    react = True
  
  elif message.author.id == 1110922698382647356: # Lette
    guild = await bot.fetch_guild(1035115107178512384)
    emoji = await guild.fetch_emoji(1083499572409675949) # alarm
    react = True

  elif message.author.id == 1137508805106737243: # Silver
    guild = await bot.fetch_guild(1035115107178512384)
    emoji = await guild.fetch_emoji(1137508805106737243) # dino dance
    react = True
  
  elif message.author.id == 569277281046888488: # nMarkov
    guild = await bot.fetch_guild(1030592458209366156)
    emoji = await guild.fetch_emoji(1151853509378064435) # Funny bee emoji
    react = True

  elif message.author.id == 1112348830034296852: # Destin
    guild = await bot.fetch_guild(1035115107178512384)
    emoji = await guild.fetch_emoji(1049756255629090856) # Irishfuck
    react = True
  
  elif message.author.id == 980341109983170570: # Ske
    guild = await bot.fetch_guild(1030592458209366156)
    emoji = await guild.fetch_emoji(1154096962845548544) # me irl
    emoji = discord.PartialEmoji(name="🐌")
    react = True

  elif message.author.id == 1000470934710403082: # Aexel
    #emoji = discord.PartialEmoji(name="🐵")
    react = False
  
  elif message.author.id == 1155555644284358727: # sisyphus prime
    guild = await bot.fetch_guild(1076022921195167744)
    emoji = await guild.fetch_emoji(1076428068811456523) # joseph_carlo
    react = True

  if react:  
    try:
      await message.add_reaction(emoji)
    except discord.errors.Forbidden:
      pass
    except discord.errors.NotFound:
      pass

bot.run(token)
