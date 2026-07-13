import sys, time
print("Step 1: imports done", flush=True)

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

print("Step 2: creating session, this may take 20-40s...", flush=True)

PACKAGE_NAME = "com.santa.web3.browser_qa"
APP_ACTIVITY = "com.google.android.apps.chrome.Main"
APPIUM_SERVER = "http://127.0.0.1:4723"

AD_CONTAINER_XPATH = '//android.view.ViewGroup[contains(@resource-id, ":id/ad_personalization")]'

BANNER_LOCATORS = [
    (
        "Google AdMob",
        AppiumBy.XPATH,
        AD_CONTAINER_XPATH
        + "/android.widget.FrameLayout/android.widget.FrameLayout"
        + "/android.widget.FrameLayout/android.webkit.WebView",
    ),
    (
        "Google AdMob text",
        AppiumBy.XPATH,
        AD_CONTAINER_XPATH
        + "/android.widget.FrameLayout/android.widget.FrameLayout"
        + "/android.widget.FrameLayout/android.webkit.WebView//android.widget.TextView",
    ),
    (
        "Vungle",
        AppiumBy.XPATH,
        AD_CONTAINER_XPATH
        + "/android.widget.FrameLayout/android.widget.RelativeLayout",
    ),
    (
        "Vungle image",
        AppiumBy.XPATH,
        AD_CONTAINER_XPATH
        + "/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.ImageView",
    ),
    (
        "InMobi",
        AppiumBy.XPATH,
        AD_CONTAINER_XPATH
        + "/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout",
    ),
    (
        "InMobi WebView",
        AppiumBy.XPATH,
        AD_CONTAINER_XPATH
        + "/android.widget.FrameLayout/android.widget.FrameLayout"
        + "/android.widget.RelativeLayout/android.webkit.WebView",
    ),
    (
        "Any WebView ad banner",
        AppiumBy.XPATH,
        AD_CONTAINER_XPATH + "//android.webkit.WebView",
    ),
    (
        "Any ad personalization banner",
        AppiumBy.XPATH,
        AD_CONTAINER_XPATH,
    ),
]


def find_visible_banner(wait):
    for banner_name, by, locator in BANNER_LOCATORS:
        try:
            banner_wait = WebDriverWait(driver, 4)
            banner_element = banner_wait.until(
                EC.visibility_of_element_located((by, locator))
            )

            if banner_element.is_displayed():
                print(f"Step 3: {banner_name} banner found.", flush=True)
                return banner_element

        except TimeoutException:
            print(f"{banner_name} banner not found. Trying next banner type...", flush=True)

    raise TimeoutException("No supported ad banner was visible.")

options = UiAutomator2Options()
options.platform_name = "Android"
options.device_name = "Android Device"
options.app_package = PACKAGE_NAME
options.app_activity = APP_ACTIVITY
options.no_reset = True
options.automation_name = "UiAutomator2"

driver = webdriver.Remote(APPIUM_SERVER, options=options)
TEST_PASSED = False

try:
    wait = WebDriverWait(driver, 20)

    time.sleep(3)

    banner = find_visible_banner(wait)

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
    TEST_PASSED = True

except TimeoutException:
    print("TIMEOUT - banner not found, dumping page source", flush=True)
    print(driver.page_source)

except Exception as e:
    print(f"UNEXPECTED ERROR: {e}", flush=True)
    print(driver.page_source)

if not TEST_PASSED:
    print("\n========== TEST RESULT: FAILED ==========", flush=True)
    driver.quit()
    sys.exit(1)

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

print("\n========== TEST RESULT: PASSED ==========", flush=True)

driver.quit()
