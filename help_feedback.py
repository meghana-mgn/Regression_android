from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ---------------- Desired Capabilities ----------------

options = UiAutomator2Options()

options.platform_name = "Android"
options.device_name = "Android"
options.automation_name = "UiAutomator2"
options.app_package = "com.santa.web3.browser"
options.app_activity = "com.santa.web3.browser.MainActivity"

# Don't reset app data
options.no_reset = True

# ---------------- Start Driver ----------------

driver = webdriver.Remote(
    "http://127.0.0.1:4723",
    options=options
)

wait = WebDriverWait(driver, 20)

try:
    print("Waiting for Help & feedback...")

    help_button = wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.ID, "com.santa.web3.browser:id/help_id")
        )
    )

    help_button.click()

    print("SUCCESS - Help & feedback clicked.")

    time.sleep(5)

except Exception as e:
    print("TIMEOUT - Required element not found.")
    print(e)

finally:
    driver.quit()