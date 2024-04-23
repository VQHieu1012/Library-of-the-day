import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
 
 
async def main():
    # Launch the Playwright instance
    async with async_playwright() as playwright:
        # Launch the browser
        browser = await playwright.firefox.launch_persistent_context(user_data_dir='C:\\Users\\admin\\AppData\\Local\\Google\\Chrome\\User Data\\', headless=False)
 
        page = await browser.new_page()

 
        # Apply stealth to the page
        await stealth_async(page)
 
        # Navigate to the desired URL
        await page.goto("https://nowsecure.nl/")
        await page.wait_for_timeout(5000)
        await page.reload()
        await page.wait_for_timeout(30000)
 
        # Wait for any dynamic content to load
        await page.wait_for_load_state("networkidle")
    
        # Take a screenshot of the page
        await page.screenshot(path="nowsecure_success.png")
 
        # Retrieve the desired element
        elements = await page.query_selector_all("h1")
        if elements:
            text_content = await elements.inner_text()
            print(text_content)
        
 
        # Close the browser
        await browser.close()
 
# Run the main function
asyncio.run(main())
