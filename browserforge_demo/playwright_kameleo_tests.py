#THIS IS A TEMPLATE SPIDER FOR WHAT WE CALL PHASE A
#ITEMS, LOGGING SYSTEM AND OUTPUT FILES WILL HAVE ALWAYS THE 
#SAME STRUCTURE AND BEHAVIOUR FOR EVERY SPIDER IN PHASE A


from kameleo.local_api_client import KameleoLocalApiClient
from kameleo.local_api_client.builder_for_create_profile import BuilderForCreateProfile
from playwright.sync_api import sync_playwright
import time
import csv
from random import randrange
import random
from datetime import datetime


client = KameleoLocalApiClient(
	endpoint='http://IP:5050',
	retry_total=0
)

# Start the browser profile
profile_id=''
client.start_profile(profile_id)

with sync_playwright() as p:
	browser_ws_endpoint = 'ws://IP:5050/playwright/'+profile_id
	browser = p.chromium.connect_over_cdp(endpoint_url=browser_ws_endpoint)
	default_context = browser.contexts[0]
	page = default_context.pages[0]
	page.goto('https://www.browserscan.net/en', timeout=0)
	interval=randrange(50)
	time.sleep(interval)
	page.goto('https://www.harrods.com/')  # Navigate to the target website
	time.sleep(10)
	page.goto('https://www.harrods.com/en-de/shopping/women')  # Navigate to the target website
	time.sleep(50)
	page.goto('https://www.footlocker.it/')  # Navigate to the target website
	time.sleep(10)
	page.goto('https://www.footlocker.it/it/category/donna/accessori.html')  # Navigate to the target website
	time.sleep(50)
	page.goto('https://stockx.com/')  # Navigate to the target website
	time.sleep(10)
	page.goto('https://stockx.com/sneakers?size_types=men')  # Navigate to the target website
	time.sleep(50)
	client.stop_profile(profile_id)
	browser.close()

