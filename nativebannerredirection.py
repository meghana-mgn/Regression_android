import sys, time
print("Step 1: imports done", flush=True)

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

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
    wait = WebDriverWait(driver, 20)

    time.sleep(3)

    banner = None

    # ==========================================================
    # Try Google Ads banner first
    # ==========================================================

    try:
        banner = wait.until(
            EC.presence_of_element_located(
                (
                    AppiumBy.XPATH,
                    '//android.view.ViewGroup[@resource-id="com.santa.web3.browser:id/ad_personalization"]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.widget.TextView'
                )
            )
        )

        print("Step 3: Google Ads banner found.", flush=True)

    except Exception:
        print("Google Ads banner not found. Trying Vungle...", flush=True)

    # ==========================================================
    # If Google banner not found, try Vungle banner
    # ==========================================================

    if banner is None:
        banner = wait.until(
            EC.presence_of_element_located(
                (
                    AppiumBy.XPATH,
                    '//android.view.ViewGroup[@resource-id="com.santa.web3.browser:id/ad_personalization"]/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.ImageView'
                )
            )
        )

        print("Step 3: Vungle banner found.", flush=True)

    # ==========================================================
    # Tap center of banner (DO NOT call banner.click())
    # ==========================================================

    location = banner.location
    size = banner.size

    center_x = location["x"] + size["width"] // 2
    center_y = location["y"] + size["height"] // 2

    print(f"Banner center = ({center_x}, {center_y})", flush=True)

    driver.tap([(center_x, center_y)])

    print("Step 4: Banner center tapped successfully.", flush=True)

    time.sleep(5)

except TimeoutException:
    print("TIMEOUT - banner not found, dumping page source", flush=True)
    print(driver.page_source)

except Exception as e:
    print(f"UNEXPECTED ERROR: {e}", flush=True)
    print(driver.page_source)

# ==========================================================
# Open Recents
# ==========================================================

driver.press_keycode(187)
print("Step 5: Opened Recents screen.", flush=True)

time.sleep(2)

# ==========================================================
# Reopen Santa Browser
# ==========================================================

wait = WebDriverWait(driver, 15)

santa_card = wait.until(
    EC.element_to_be_clickable(
        (
            AppiumBy.XPATH,
            '//*[contains(@text,"Santa") or contains(@content-desc,"Santa")]'
        )
    )
)

santa_card.click()

print("Step 6: Santa Browser reopened from Recents.", flush=True)

driver.quit()