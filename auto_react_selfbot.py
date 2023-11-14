# This only works on bash's curl due to how cmd and powershell do stuff with formatting when parsing
# Use WSL if you are on windows. Download it in the store here https://apps.microsoft.com/search?query=wsl
# Or you can try and debug it so that it works in windows. I tried for a bit but could not get it to work

selfbot_token = "" # The token of the account you want to react with (needs nitro)
normalbot_token = "" 
# Token of bot that is in the server
# We use a normal bot to detect messages as that is far easier
# Also I could not be bothered to code a websocket for a selfbot so that we can be a full selfbot

your_id = 667276333294026772
# The id of the user you want to react to

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
# User agent given to discord so they are less likely to ban us


emoji_name = "lightsaberpepe"
emoji_id = 1164255035174178896

your_id = 0
on_your_messages = False # Every message you send gets a react
on_your_mentions = True # Every message that mentions you or replies to you gets a react


# Do not need to change anything past here
import os
import discord
import base64



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

web_head1 = r'''--header "Content-Length: 0" --header "Dnt: 1"  --header "Origin: https://discord.com" '''
web_head3 = f'''"Not=A?Brand";v="99" --header "Sec-Ch-Ua-Platform: 'Windows'" --header "x-super-properties: {super_properties_final}"'''
token_header = f' --header "Authorization: {selfbot_token}"'
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
  
  react = False
  for m in message.mentions:
    if m.id == your_id and on_your_mentions:
      react = True

  if message.author.id == your_id and on_your_messages:
    react = True

  if react:
    web_head2 = f'''--header "Referer: https://discord.com/channels/{message.guild.id}/{message.channel.id}" --header '"Google Chrome";v="{browser_version[1]}", "Chromium";v="{browser_version[1]}", '''
    web_headers = f'--user-agent "{user_agent}" ' + web_head1 + web_head2 + web_head3 + token_header
    os.system(f'''curl -X PUT "{base_url}/channels/{message.channel.id}/messages/{message.id}/reactions/{emoji_name}%3A{emoji_id}/%40me?location=Message&type=1" {web_headers}''')


bot.run(normalbot_token)
