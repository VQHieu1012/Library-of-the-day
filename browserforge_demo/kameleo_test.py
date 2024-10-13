
from kameleo.local_api_client import KameleoLocalApiClient
from kameleo.local_api_client.builder_for_create_profile import BuilderForCreateProfile
from playwright.sync_api import sync_playwright
import time
from random import randrange
import random
from datetime import datetime

# This is the port Kameleo.CLI is listening on. Default value is 5050, but can be overridden in appsettings.json file
kameleo_port = 5050

client = KameleoLocalApiClient(
	endpoint='http://IP:5050',
	retry_total=0
)

# Search Chrome Base Profiles
#base_profiles = client.search_base_profiles(
#	device_type='desktop',
#	browser_product='chrome',
#	os_family='windows'
#	
#)

# Create a new profile with recommended settings
# Choose one of the Base Profiles
#create_profile_request = BuilderForCreateProfile \
#	.for_base_profile(base_profiles[0].id) \
#	.set_recommended_defaults() \
#	.build()
#profile = client.create_profile(body=create_profile_request)

# Start the browser profile
profile=''
client.start_profile(profile)
print(profile)
# Connect to the browser with Playwright through CDP
browser_ws_endpoint = f'ws://IP:{kameleo_port}/playwright/{profile}'
with sync_playwright() as playwright:
	browser = playwright.chromium.connect_over_cdp(endpoint_url=browser_ws_endpoint)
	context = browser.contexts[0]
	page = context.new_page()

	# Use any Playwright command to drive the browser
	# and enjoy full protection from bot detection products
	page.goto('https://www.browserscan.net/en')
	interval=randrange(10,30)
	time.sleep(50)
	

# Wait for 5 seconds
time.sleep(5)

# Stop the browser by stopping the Kameleo profile
client.stop_profile(profile.id)