import sys, time
print("Step 1: imports done", flush=True)
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
print("Step 2: creating session, this may take 20-40s...", flush=True)
PACKAGE_NAME = "com.santa.web3.browser"
APP_ACTIVITY = "com.google.android.apps.chrome.Main"
APPIUM_SERVER = "http://127.0.0.1:4723"
options = UiAutomator2Options()
options.platform_name = "Android"
options.device_name = "Android Device"
options.app_package = PACKAGE_NAME
options.app_activity = APP_ACTIVITY
options.no_reset = True
options.automation_name = "UiAutomator2"
driver = webdriver.Remote(APPIUM_SERVER, options=options)
try:
    wait = WebDriverWait(driver, 15)
    time.sleep(2)  # let the homepage/banner fully render after launch

    banner = wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.XPATH,
             '//android.view.ViewGroup[@resource-id="com.santa.web3.browser:id/ad_personalization"]/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.ImageView')
        )
    )
    banner.click()
    print("Step 4: Banner clicked, redirection triggered successfully.", flush=True)

    time.sleep(2)  # give the redirect time to complete

except TimeoutException:
    print("TIMEOUT - banner not found, dumping page source for inspection", flush=True)
    print(driver.page_source)

    # --- Open Recents ---
driver.press_keycode(187)
print("Opened Recents screen.", flush=True)
time.sleep(2)

# --- Tap Santa Browser's card to reopen it ---
# NOTE: exact locator depends on your device's Recents UI (see below)
santa_card = wait.until(
    EC.element_to_be_clickable(
        (AppiumBy.XPATH, '//*[contains(@text,"Santa") or contains(@content-desc,"Santa")]')
    )
)
santa_card.click()
print("Tapped Santa Browser card in Recents, app reopened.", flush=True)