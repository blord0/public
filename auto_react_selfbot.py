# The user agent value is the only that that needs to be updated from time to time
# Copy the value given from this url https://www.google.com/search?q=what+is+my+user+agent
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
token_selfbot = ""
token_bot = ""

# Needs normal bot and selfbot bc i cba to make a websocket for message events

import discord
import base64
import requests

base_url = "https://discord.com/api/v9"
for c in range(len(user_agent)):
  if user_agent[c:c+6] == "Chrome":
    temp_start = c+7
    break

majorFound = False
for c in range(temp_start, len(user_agent)):
  if user_agent[c] == " ":
    browser_version = [user_agent[temp_start:c], user_agent[temp_start:majorFound]]
    break
  if not majorFound and user_agent[c] == ".":
    majorFound = c

super_properties_build = r'{"os":"Windows","browser":"Chrome","device":"","system_locale":"en-GB","browser_user_agent":"'
super_properties_build += user_agent + f'","browser_version":"{browser_version[0]}","os_version":"10",'
super_properties_build += r'"referrer":"","referring_domain":"","referrer_current":"","referring_domain_current":"",'
super_properties_build += r'"release_channel":"stable","client_build_number":244358,"client_event_source":null,"design_id":0}'
super_properties_build = super_properties_build.encode("ascii")
super_properties_final = str(base64.b64encode(super_properties_build))[2:-1]

web_headers = {"Content-Type": "application/json", "Dnt": "1", "Origin": "https://discord.com", "Referer": "https://discord.com/channels/@me", 
               "Sec-Ch-Ua": f'"Google Chrome";v="{browser_version[1]}", "Chromium";v="{browser_version[1]}", "Not=A?Brand";v="99"',
               "Sec-Ch-Ua-Platform": "'Windows'", "x-super-properties": super_properties_final, "user-agent": user_agent,
               "Authorization": token_selfbot
               }

bot = discord.Client(intents=discord.Intents.all())

@bot.event
async def on_ready():
  print(f"Hooked into {bot.user}")
  print(f"Running autoreact")

@bot.event
async def on_message(message: discord.Message):
  if message.interaction:
    if type(message.interaction.user) == discord.User:
      return
  for m in message.mentions:
    react = False
    if m.id == 667276333294026772: # blord
      emoji_var = r"lightsaberpepe%3A1164255035174178896"
      react = True
    elif m.id == 1110922698382647356: #lette
      emoji_var = r"alarm%3A1083499572409675949"
      react = True
    elif m.id == 1112874692190150757: # 33plus0
      emoji_var = r"33plus0%3A1056248100265664562"
      react = True
    elif m.id == 436089192259387393: # Noah
      emoji_var = r"amogussex%3A1171896310689955960"
      react = True
    elif m.id in [1125525137689694368, 549207190330671107]: # Diavolo and violent
      emoji_var = r"thugass%3A1165776586889502861"
      react = True
    elif m.id == 1111505015308304384: # Jayden
      emoji_var = r"%F0%9F%87%B3%F0%9F%87%BF"
      react = True

    if react:
      web_headers["Referer"] = f"https://discord.com/channels/{message.guild.id}/{message.channel.id}"
      req_url = f"{base_url}/channels/{message.channel.id}/messages/{message.id}/reactions/{emoji_var}/%40me?location=Message&type=1"
      var = requests.api.request("PUT", req_url, headers=web_headers).content
      if str(var) != "b''":
        print(var)

# Code only runs in wacko cracko server

bot.run(token_bot)
