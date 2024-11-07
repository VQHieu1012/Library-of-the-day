from undetected_playwright.sync_api import sync_playwright
import time



def run_playwright_patched(playwright):
	args = []
	args.append("--disable-blink-features=AutomationControlled")
	args.append("--start-maximized")

	browser = playwright.chromium.launch(args=args, headless=False)  # Launch browser
	page = browser.new_page(no_viewport=True)
	page.evaluate("""
			(function() {
				// Lưu trữ hàm toString ban đầu của Date
				const originalToString = Date.prototype.toString;

				// Ghi đè hàm toString để loại bỏ phần (Indochina Time)
				Date.prototype.toString = function() {
					const originalString = originalToString.call(this);
					return originalString.replace(/\(.*\)/, '');
				};
			})();
		""")
	page.goto('https://www.browserscan.net/')  # Navigate to the target website
	time.sleep(10)
	page.screenshot(path="screenshot_patched.png")
	time.sleep(50)
	browser.close()

with sync_playwright() as playwright:
	run_playwright_patched(playwright)