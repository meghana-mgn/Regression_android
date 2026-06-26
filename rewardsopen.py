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
    rewards_btn = wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.ID, "com.santa.web3.browser:id/rewards_btn")
        )
    )
    rewards_btn.click()
    print("Step 3: Rewards button clicked successfully.", flush=True)

    time.sleep(2)  # let the rewards page finish loading after redirect

    plus_btn = wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.ID, "com.santa.web3.browser:id/optional_toolbar_button")
        )
    )
    plus_btn.click()
    print("Step 4: '+' button clicked successfully.", flush=True)

except TimeoutException:
    print("TIMEOUT - dumping current page source for inspection", flush=True)
    print(driver.page_source)