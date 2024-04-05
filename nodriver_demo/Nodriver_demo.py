import asyncio
import nodriver as uc
import numpy as np
from bs4 import BeautifulSoup as bs

"""
This is the demo code for using Nodriver to scrape products from Shopee.
However, we should respect the website, both in terms of its terms of service and its server resources.
Since Nodriver is fully asynchronous, it is blazing fast which can lead to unpredictable behavior.
For that reason, I always add 'delay' between lines of code. 
If you want your scraper run faster, you can modify delay time.
I also set 'headless=False' to see what actually happens when we run the scraper.
Result: Nodriver does its best to bypass many types of bot-detection. I think you should give it a try in your project.

Visit source code: https://github.com/ultrafunkamsterdam/nodriver for more infomation.

Note: This code is rarely updated since it is just a demo.
"""


async def main():
    LINK = 'https://shopee.vn/'

    # Path to your chrome user data
    USER_DATA_DIR = '' #'C:\\Users\\admin\\AppData\\Local\\Google\\Chrome\\User Data\\'

    # your shoppe account
    ACCOUNT = 'your account'

    # your shopee password
    PASSWORD = 'your password'

    # keyword to search
    KEYWORD_TO_SEARCH = 'bitis hunter'

    browser = await uc.start(user_data_dir=USER_DATA_DIR)

    page = await browser.get(LINK)

    await page.sleep(np.random.randint(1, 3))
    await page # wait for event to finish

    # await page.wait_for(page.find('Email/Số điện thoại/Tên đăng nhập'))

    # Check if sign in or not
    try:
        account = await page.find('Email/Số điện thoại/')
        await account.send_keys(ACCOUNT)
        await page.sleep(np.random.randint(1, 3))

        password = await page.find_element_by_text('Mật khẩu')
        await password.send_keys(PASSWORD)
        await page.sleep(np.random.randint(1, 3))

        enter = await page.select('button[class="DYKctS hqfBzL SYqMlu NBaRN4 CEiA6B ukVXpA"]')
        await enter.click()
        await page.sleep(np.random.randint(1, 5))
    except:
        print('Already sign in.')

    # send keyword to search bar
    search = await page.select('input[class="shopee-searchbar-input__input"]')
    await search.send_keys(KEYWORD_TO_SEARCH)
    btn = await page.select('button[class="btn btn-solid-primary btn--s btn--inline shopee-searchbar__search-button"]')
    await btn.click()
    await page.sleep(5)
    
    page_num = 1
    # loop through all pages until done (or maybe get blocked by captcha) 
    # (check last_image.jpg to see if it reaches the last page or gets block)
    
    links = [] # initialize a list to store all products' link

    while True:
        
        # scroll down to get fully rendered JS
        for _ in range(4):
            await page.scroll_down(np.random.randint(150, 200))
            await page.sleep(np.random.uniform(1, 3))  
        
        try:
            soup = bs(await page.get_content(), 'lxml')
            link = soup.find_all('a', class_='contents')
            links.extend("https://shopee.vn" + i.get('href') for i in link)

            next = await page.select('a[class="shopee-icon-button shopee-icon-button--right"]')
            await next.scroll_into_view()
            await next.click()
            page_num += 1
            print('Current page:', page_num)
            await page.sleep(np.random.uniform(1, 3))
        except:
            print("Open last_image.jpg to check if you reach your last page or get block by captcha")
            await page.save_screenshot('.//last_image.jpg')       
            break 
    print('Number of product links:', len(links))
    # We navigate through each link in links 
    for link in links:
        await page.get(link)
        await page

        for _ in range(5):
            # slowly scroll down to get fully rendered Javascript
            await page.scroll_down(np.random.randint(200, 350))
            await page.sleep(np.random.uniform(1, 3))

        await page.sleep(np.random.uniform(1, 3))    
        # From here, you can customize your code to extract data you need.
        # It is easier to stick with BeautifulSoup or you can integrate nodriver with Scrapy also.
    
if __name__ == '__main__':
    uc.loop().run_until_complete(main())
