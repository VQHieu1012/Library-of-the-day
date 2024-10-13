from playwright.sync_api import sync_playwright
import time
from random import randrange
from browserforge.injectors.playwright import NewContext
from browserforge.fingerprints import FingerprintGenerator


def run(playwright):
	CHROMIUM_ARGS= [
			'--no-first-run',
			'--disable-blink-features=AutomationControlled',
			'--force-webrtc-ip-handling-policy'
		  ]
		  
	proxy={
	  "server": "",
	  "username": "",
	  "password": ""
	}
	
	browser = playwright.chromium.launch(proxy=proxy, headless=False,slow_mo=200, args=CHROMIUM_ARGS,ignore_default_args=["--enable-automation"])  # Launch browser
	context = browser.new_context(
		permissions=['geolocation']  # Grant permissions for geolocation
	)
	page = context.new_page()
	page.goto('https://www.browserscan.net/en')  # Navigate to the target website
	time.sleep(50)
	context.close()
	browser.close()

#with sync_playwrigz44ht() as playwright:
#	run(playwright)


def run_mocked(playwright):
	CHROMIUM_ARGS= [
			'--no-first-run',
			'--disable-blink-features=AutomationControlled',
		  ]
	proxy={
	  "server": "",
	  "username": "",
	  "password": ""
	}
	
	browser = playwright.chromium.launch(proxy=proxy,headless=False,slow_mo=200, args=CHROMIUM_ARGS,ignore_default_args=["--enable-automation"])
	# Create a new context with the injected fingerprint
	
	context = NewContext(browser,fingerprint_options ={'browser':'firefox', 'os':'windows'})
	page = context.new_page()
	page.goto('https://www.browserscan.net/en')  # Navigate to the target website
	time.sleep(50)
	context.close()
	browser.close()

#with sync_playwright() as playwright:
#	run_mocked(playwright)  
	
	

def run_mocked_with_location(playwright):
	CHROMIUM_ARGS= [
			'--no-first-run',
			'--disable-blink-features=AutomationControlled',
		  ]
	proxy={
	  "server": "",
	  "username": "",
	  "password": ""
	}
	
	browser = playwright.firefox.launch(proxy=proxy,headless=False,slow_mo=200, args=CHROMIUM_ARGS,ignore_default_args=["--enable-automation"])
	# Create a new context with the injected fingerprint
	
	context = NewContext(browser,fingerprint_options ={'browser':'firefox', 'os':'windows'})
	page = context.new_page()
	page.goto('https://www.browserscan.net/en')  # Navigate to the target website
	time.sleep(50)
	context.close()
	browser.close()

with sync_playwright() as playwright:
	run_mocked_with_location(playwright)  