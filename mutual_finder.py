import discord
import os

bot = discord.Client(intents=discord.Intents.all())

def sort_algo(e: discord.Guild):
  return e.member_count
# https://www.w3schools.com/python/ref_list_sort.asp

find_user = input("Input user: ") # Can be username or id

@bot.event
async def on_ready():
  global find_user
  guild_list: list[discord.Guild] = []
  for guild in bot.guilds:
    guild_list.append(guild)

  guild_list.sort(key=sort_algo, reverse=True)

  try:
    find_user = int(find_user)
  except ValueError:
    if type(find_user) == str:
      for i in bot.users:
        if i.name == find_user:
          find_user = i.id
          print(f"Id is {find_user}")
          break
      else:
        print("Couldn't find that user")
        os.kill(os.getpid())

  mutual_list: list[discord.Guild] = []
  search_user = await bot.fetch_user(find_user)
  print(f"Looking for {search_user.name}")
  for i in range(len(guild_list)):
    guild = guild_list[i]
    async for user in guild.fetch_members(limit=None):
      if user.id == search_user.id:
        mutual_list.append(guild)
  
  print(f"{search_user.name} is in {len(mutual_list)}/{len(guild_list)} of our guilds")
  if len(mutual_list) == 0:
    os.kill(os.getpid(), 9)
  
  longest_n = 0
  largest = mutual_list[0]
  largest_c = len(str(largest.member_count))

  for i in mutual_list:
    if len(i.name) > longest_n:
      longest_n = len(i.name)

  table = ""
  for i in range(longest_n + largest_c):
    table += "-"
  table += "-------\n"

  # All of that is for adding first line of table

  for i in mutual_list:
    i.name = f"{i.name:{''}{longest_n}}"

  for i in range(len(mutual_list)):
    table += f"| {mutual_list[i].name} | {mutual_list[i].member_count:0{largest_c}d} |\n"

  for i in range(longest_n + largest_c):
    table += "-"
  table += "-------"

  print(table)

  os.kill(os.getpid(), 9)

bot.run(token)
