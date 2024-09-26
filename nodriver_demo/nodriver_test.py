import nodriver as uc
import json
import time

async def main():
    # Start the headless browser
    browser = await uc.start(headless=False,no_sandbox=True,user_data_dir="C:\\Users\\admin\\AppData\\Local\\Google\\Chrome\\User Data\\", lang="en-US")
    time.sleep(30)
    page = await browser.get(
        "https://deviceandbrowserinfo.com/info_device"
    )

    time.sleep(60)

    # Stopping the headless browser
    browser.stop()

if __name__ == "__main__":
    # Running the main function
    uc.loop().run_until_complete(main())
