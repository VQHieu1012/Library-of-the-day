from playwright.sync_api import sync_playwright
import time



def run_playwright_vanilla(playwright):
	args = []
	# disable navigator.webdriver:true flag
	args.append("--disable-blink-features=AutomationControlled")
	args.append("--start-maximized")

	browser = playwright.chromium.launch(args=args, headless=False)  # Launch browser
	page = browser.new_page(no_viewport=True)
	page.goto('https://www.browserscan.net/')  # Navigate to the target website
	time.sleep(10)
	page.screenshot(path="screenshot_vanilla.png")
	time.sleep(50)
	browser.close()

with sync_playwright() as playwright:
	run_playwright_vanilla(playwright)