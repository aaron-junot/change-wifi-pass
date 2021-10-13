from dotenv import load_dotenv

import os
import random
import requests
import urllib.parse
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

# Get the Environment Variables we need
creds = os.getenv('ROUTER_CREDENTIALS')
ip = os.getenv('ROUTER_IP')
port = os.getenv('ROUTER_PORT')
url_plus_encoded_ssid = os.getenv("URL_PLUS_ENCODED_SSID")
url_encoded_ssid = os.getenv("URL_ENCODED_SSID")
double_encoded_old_password = urllib.parse.quote_plus(urllib.parse.quote_plus(os.getenv("OLD_PASSWORD")))
model = os.getenv("MODEL_NUMBER")
slack_token = os.getenv("SLACK_TOKEN")
slack_channel = os.getenv("SLACK_CHANNEL")

# Get a session with the router
headers = {'Referer': f"https://{ip}:{port}/Main_Login.asp", 'Content-Type': 'application/x-www-form-urlencoded'}
params = f"login_authorization={urllib.parse.quote(creds)}"

s = requests.Session()
r = s.post(f"https://{ip}:{port}/login.cgi", headers=headers, data=params, verify=False)


# Create a new password
words = open("wordlist.txt", "r").read().splitlines()
new_password = random.choice(words).capitalize() + random.choice(words).capitalize()
# TODO: Make sure new_password is >7 characters because a Fire Tablet for kids requires 8 characters for the PSK


# Tell the router to update the password
payload = (f"current_page=%2F&next_page=%2F&action_mode=apply_new&action_script=restart_wireless" +
f"&action_wait=8&productid={model}&wps_enable=0&wsc_config_state=1&wl_ssid_org={url_plus_encoded_ssid}" +
f"&wl_wpa_psk_org={double_encoded_old_password}&wl_auth_mode_orig=pskpsk2&wl_nmode_x=0&wps_band=0" +
f"&wl_unit=0&wl_mfp=1&wl_subunit=-1&smart_connect_x=0&smart_connect_t=0&wl_ssid={url_encoded_ssid}" +
f"&wl_auth_mode_x=pskpsk2&wl_crypto=aes&wl_wpa_psk={new_password}")

headers = {'Referer': f"https://{ip}:{port}/device-map/router.asp", 'Content-Type': 'application/x-www-form-urlencoded'}

r = s.post(f"https://{ip}:{port}/start_apply2.htm", headers=headers, data=payload, verify=False)


# Post the new password to Slack
params = {
    'token': slack_token,
    'channel': slack_channel,
    'text': f"New Wi-Fi Password: {new_password}",
}
r = requests.post("https://slack.com/api/chat.postMessage", params=params)
