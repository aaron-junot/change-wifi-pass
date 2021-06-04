from dotenv import load_dotenv

import os
import requests

load_dotenv()

print(os.getenv('ROUTER_CREDENTIALS'))
print(os.getenv('ROUTER_IP'))
print(os.getenv('ROUTER_PORT'))

