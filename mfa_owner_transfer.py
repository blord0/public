# This script does not work on windows due to how cmd parses the commands
# You can install wsl here https://apps.microsoft.com/search?query=wsl
# Then start wsl and launch the python script from there
# You can try get it to work with Windows cmd but I have no idea how you would do that

import os
import json
import base64

token = input("Token of owner: ")
recipient_id = input("User ID of recepient: ")
guild_id = input("Guild ID you want to transfer: ")
two_fa = input("2FA code from app: ")

base_url = "https://discord.com/api/v9"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"

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
super_properties_build += r'"release_channel":"stable","client_build_number":245361,"client_event_source":null,"design_id":0}'
super_properties_build = super_properties_build.encode("ascii")

super_properties_final = str(base64.b64encode(super_properties_build))[2:-1]

web_head1 = r'''--header "Content-Type: application/json" --header "Dnt: 1"  --header "Origin: https://discord.com" '''
web_head2 = f'''--header "Referer: https://discord.com/channels/@me" --header '"Google Chrome";v="{browser_version[1]}", "Chromium";v="{browser_version[1]}", "Not=A?Brand";v="99"' '''
web_head3 = f'''--header "Sec-Ch-Ua-Platform: 'Windows'" --header "x-super-properties: {super_properties_final}"'''
web_headers = f'--user-agent "{user_agent}" ' + web_head1 + web_head2 + web_head3



extra_data_trans_rq = r'''--data '{"owner_id": "''' + recipient_id + r'''"}' '''.rstrip("")

web_headers += f''' --header "Authorization: {token}"'''

response_1_raw = os.popen(f"curl -s -X PATCH {base_url}/guilds/{guild_id} {web_headers} {extra_data_trans_rq}").read() # Makes a resquest to transfer owner. We expect this to fail

response_1 = json.loads(response_1_raw) # As part of the error, we get a mfa request ticket which can be used to get an mfa token
ticket = response_1["mfa"]["ticket"] # mfa stands for "Multi Factor Authentication"
print(ticket)
extra_data_mfa = r'''--data '{"ticket": "''' + ticket + r'''", "mfa_type": "totp", "data": "''' + two_fa + r'''"}' '''

response_2_raw = os.popen(f"curl -s -X POST {base_url}/mfa/finish {web_headers} {extra_data_mfa}").read()

response_2 = json.loads(response_2_raw)

mfa_token = response_2["token"] # 2fa token that gives us permission to transfer ownership

web_headers += f''' --header "cookie: __Secure-recent_mfa={mfa_token}"'''

response_3_raw = os.popen(f"curl -s -X PATCH {base_url}/guilds/{guild_id} {web_headers} {extra_data_trans_rq}").read() # Make request to discord with mfa token to transfer owner
print(f"Should have transfered token to {recipient_id}!")
