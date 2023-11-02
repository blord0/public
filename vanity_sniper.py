# Bot cannot change the server's vanity url so this can only announce when it is available

annouce_channel = 1042879148726685737 # The channel where the bot will send the message
user_ping_id_list = [667276333294026772] # Add the ids of who should be pinged

snipe_url = "memehub" # The url you want to check
time_wait = 60 # How often in seconds you want to check the url (be careful of discord rate limiting)


import discord
import datetime
import subprocess
import time

def current_time():
  """Formats time to `hh:mm` and returns it"""
  hour = str(datetime.datetime.now().hour)
  minute = str(datetime.datetime.now().minute)
  if len(hour) == 1:
    hour = "0" + hour
  if len(minute) == 1:
    minute = "0" + minute
  return f"{hour}:{minute}"

message_ping = ""
for i in user_ping_id_list:
  message_ping += f"<@{i}> "


bot = discord.Client(intents=discord.Intents.default())

@bot.event
async def on_ready():
  alert_channel = await bot.fetch_channel(annouce_channel)
  for i in range(5):
    await alert_channel.send(f"discord.gg/{snipe_url} is free {message_ping}")

done = False

while not done:
  status = subprocess.check_output(['curl', '-s', f'https://discord.com/api/v9/invites/{snipe_url}']).decode()
  if status != r'{"message": "Unknown Invite", "code": 10006}':
    print(f"{current_time()}: Custom url is taken")
    time.sleep(time_wait)
  else:
    print("Url is free")
    bot.run(token)

    done = True
