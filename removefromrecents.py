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
    time.sleep(2)
    print("Step 3: Santa Browser is open and running.", flush=True)

    # --- Open Recents/App Switcher ---
    driver.press_keycode(187)
    print("Step 4: Opened Recents screen.", flush=True)
    time.sleep(2)

    # --- Swipe the app card to remove it from Recents ---
    window_size = driver.get_window_size()
    width = window_size['width']
    height = window_size['height']

    driver.execute_script("mobile: swipeGesture", {
        "left": int(width * 0.1),
        "top": int(height * 0.3),
        "width": int(width * 0.8),
        "height": int(height * 0.4),
        "direction": "up",
        "percent": 1.0
    })
    print("Step 5: Swiped app card to remove from Recents.", flush=True)
    time.sleep(2)

    # --- Reopen Santa Browser ---
    driver.activate_app(PACKAGE_NAME)
    print("Step 6: Santa Browser reopened successfully.", flush=True)

except TimeoutException:
    print("TIMEOUT - dumping page source for inspection", flush=True)
    print(driver.page_source)