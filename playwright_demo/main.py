from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from bs4 import BeautifulSoup
import pandas as pd
from utils import *
import numpy as np
import re
import time
from acc_pass import ACCOUNT, PASS, USER_DATA_DIR

facebook = 'https://www.facebook.com/?stype=lo&deoia=1&jlou=AfczHBzuFgKc5jde3dWHkPnlaB20s2OgvO2xVhdv5IidANHiSADnJtBKCyAvR6aWz5VMH83wtWkYKvxYe9USaIG-fC_7HhCmNfGXIp6jg_Ax3w&smuh=37746&lh=Ac-dfKrOH4QAtVz7HRw'

CHROMIUM_ARGS = [
    '--disable-blink-features=AutomationControlled',
]

link_post = "https://www.facebook.com/floydmayweather"
link_post_1 = "https://www.facebook.com/floydmayweather/posts/pfbid0ikrFJauU47XPwnVjvrhx8NLF66BivEMCjravWcCDLQtWMgfT5YAtnSTucf2yG96Vl"
link_post_2 = "https://www.facebook.com/photo/?fbid=1854707468301557&set=gm.1441962346399878&idorvanity=552152208714234"

def sign_out(page):
    page.locator("//div[@class='x1rg5ohu x1n2onr6 x3ajldb x1ja2u2z']").first.click(timeout=5000)
    page.wait_for_timeout(500)
    page.locator("//div[@role='listitem'][5]").click()
    page.wait_for_timeout(3000)
   
def sign_in(page):
    page.get_by_label("Email hoặc số điện thoại").locator('nth=0').press_sequentially(ACCOUNT, timeout=8000) #fill
    page.wait_for_timeout(500)

    page.get_by_label("Mật khẩu").locator('nth=1').press_sequentially(PASS, timeout=8000)
    page.wait_for_timeout(500)

    page.keyboard.press('Enter')
    page.wait_for_timeout(2000)

def load_more_comments(page):
    s = time.time()
    while True:
        try:
            btn = page.get_by_role('button', name="Xem thêm bình luận")
            btn.scroll_into_view_if_needed()
            btn.click(timeout=15000)
            print("Loading...")
        except:
            print("Time out!")
            break
    e = time.time()
    print("Full load with ", str(e-s))

def block(route):
    if route.request.resource_type in ["image", "media"]: # "stylesheet"
        route.abort()
    elif ".mp4" in route.request.url:
        route.abort()
    else:
        route.continue_()

def show_all_comments(page):
    try:
        #page.get_by_label("Viết bình luận", exact=False).click()
        page.locator("//div[@class='x6s0dn4 x78zum5 xdj266r x11i5rnm xat24cr x1mh8g0r xe0p6wg']").click(timeout=10000)
        page.wait_for_timeout(3000)
        page.get_by_role('menuitem').last.click()
        page.wait_for_timeout(3000)
    except NameError as e:
        print(e)
    #sign_out(page)

def click_read_more(page):
    class_ = '//div[@class="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f"]'
    btn = page.get_by_role('button', name = 'Xem thêm').and_(page.locator(class_)).all()
    
    print('------------')
    try:
        for _ in range(len(btn)):
            page.get_by_role('button', name = 'Xem thêm').and_(page.locator(class_)).first.click()
            page.wait_for_timeout(500)
    except Exception as e:
        print("Error in click_read_more")
        print(e)

def extract_comment(soup):
    output_json = []
    output_csv = []
    text = ''
    pattern_0 = r'/user/(\d+)/'
    pattern_1 = r'id=(\d+)'
    pattern_2 = r"https://www.facebook.com/(.*?)\?comment_id="
    comments = soup.find_all("div", class_ = 'x1y1aw1k xn6708d xwib8y2 x1ye3gou')
    for comment in comments:
        user_link = comment.find('a').get('href')
        if re.search(pattern_0, user_link):
            match = re.search(pattern_0, user_link)
            user_id = match.group(1)
        elif re.search(pattern_1, user_link):
            match = re.search(pattern_1, user_link)
            user_id = match.group(1)
        else:
            match = re.search(pattern_2, user_link)
            user_id = match.group(1)
        user = comment.find('span', class_ ='x3nfvp2').get_text()
        try:
            #cmt = comment.find('div', {'dir':'auto'}).get_text()
            cmt = comment.find('div', class_='x1lliihq xjkvuk6 x1iorvi4').get_text()
        except:
            cmt = "#sticker"

        text = ' '.join([text, cmt])
        output_json.append({"user_id": user_id, "user": user, "cmt": cmt})
        output_csv.append([user_id, user, cmt])
        #print(user_id, ' ', user, ' ', cmt)
    text = remove_stopword(text)
    return output_json, output_csv, text

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
                                user_data_dir=USER_DATA_DIR,
                                channel='chrome',
                                headless=False,
                                slow_mo=20,
                                args=CHROMIUM_ARGS,
                                ignore_default_args=['--enable-automation'])
    page = browser.new_page()
    stealth_sync(page)
    #page.route("**/*", block)  
    
     
    page.goto(facebook, timeout=0)
    page.goto(link_post_1)
    page.wait_for_timeout(2000)

    try:
        sign_in(page)
    except:
        print("Already sign in.")

    try:    
        show_all_comments(page)
        load_more_comments(page)
        click_read_more(page)
        
        page.wait_for_timeout(1000)
        soup = BeautifulSoup(page.content(), 'lxml')
        output_json, output_csv, text = extract_comment(soup)
        
        page.wait_for_timeout(np.random.randint(2000, 4000))
        sign_out(page)
        df = pd.DataFrame(output_csv)
        df.to_csv('output.csv', index=False)
        print("Save to output.csv")
    except NameError:
        sign_out(page)
        print(NameError)
        

    page.close()
    browser.close()




