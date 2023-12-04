# The user agent value is the only that that needs to be updated from time to time
# Copy the value given from this url https://www.google.com/search?q=what+is+my+user+agent
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"

import json
import base64
import requests

token = input("Token of admin: ")
guild_id = input("Guild ID you want to bulk ban on: ")
userID_list_str = input("Input list of user IDs. Seperate ID each with a space: ")
ban_reason = input("Reason for ban: ")
two_fa = input("2FA code from app: ")


userID_list = []
temp = ""
for c in userID_list_str:
  if c != " ":
    temp += c
  else:
    userID_list.append(temp)
    temp = ""

userID_list.append(temp)

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
               "Authorization": token
               }

data_dict = json.loads('''{"user_ids":"''' + str(userID_list) + r'''","delete_message_seconds":0,"reason":"''' + ban_reason + r'''"}''')

req_url = f"{base_url}/guilds/{guild_id}/bulk-ban"
response_1_raw = requests.api.request("post", req_url, headers=web_headers, json=data_dict).content.decode()  # Makes a resquest to bulk ban. We expect this to fail

response_1 = json.loads(response_1_raw) # As part of the error, we get a mfa request ticket which can be used to get an mfa token
ticket = response_1["mfa"]["ticket"] # mfa stands for "Multi Factor Authentication"


mfa_data_dict = {"ticket": ticket, "mfa_type": "topt", "data": f'"{two_fa}"'}
response_2_raw = requests.api.request("post", f"{base_url}/mfa/finish", headers=web_headers).content.decode()

response_2 = json.loads(response_2_raw)

mfa_token = response_2["token"] # mfa token that gives us permission to bulk ban

web_cookie = {"__Secure-recent_mfa": mfa_token}

response_3_raw = requests.api.request("post", req_url, headers=web_headers, cookies=web_cookie, json=data_dict).content.decode() # Make request to discord with mfa token to bulk ban
print(f"Bulk-ban was successful!")
