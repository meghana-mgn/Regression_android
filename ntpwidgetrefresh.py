import sys
import time

print("Step 1: imports done", flush=True)

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

print("Step 2: creating session...", flush=True)

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

TEST_PASSED = False

try:
    wait = WebDriverWait(driver, 20)

    # ==========================================================
    # Step 3 : Check if Refresh Balance button is visible
    # ==========================================================

    refresh_buttons = driver.find_elements(
        AppiumBy.ACCESSIBILITY_ID,
        "Refresh balance"
    )

    if len(refresh_buttons) > 0 and refresh_buttons[0].is_displayed():

        print("Step 3: Refresh Balance button is visible.", flush=True)

        refresh_buttons[0].click()

        print("Step 4: Refresh Balance button clicked.", flush=True)

        time.sleep(3)

    else:
        print("Step 3: Refresh Balance button is NOT visible.", flush=True)

    # ==========================================================
    # Step 5 : Verify Open Rewards widget is visible
    # ==========================================================

    open_rewards = wait.until(
        EC.visibility_of_element_located(
            (
                AppiumBy.XPATH,
                '//android.view.View[@content-desc="Open rewards"]'
            )
        )
    )

    assert open_rewards.is_displayed(), \
        "'Open rewards' widget is not visible."

    print("Step 5: Open Rewards widget is visible.", flush=True)

    # ==========================================================
    # Step 6 : Verify NTP is visible
    # ==========================================================

    ntp = wait.until(
        EC.visibility_of_element_located(
            (
                AppiumBy.XPATH,
                '//android.view.View[@resource-id="root"]/android.view.View'
            )
        )
    )

    assert ntp.is_displayed(), \
        "NTP is not visible."

    print("Step 6: NTP is visible.", flush=True)

    TEST_PASSED = True

except TimeoutException:
    print("TIMEOUT - Required element not found.", flush=True)
    print(driver.page_source)
    TEST_PASSED = False

except AssertionError as e:
    print(f"ASSERTION FAILED: {e}", flush=True)
    print(driver.page_source)
    TEST_PASSED = False

except Exception as e:
    print(f"UNEXPECTED ERROR: {e}", flush=True)
    print(driver.page_source)
    TEST_PASSED = False

finally:
    if TEST_PASSED:
        print("\n========== TEST RESULT: PASSED ✅ ==========", flush=True)
    else:
        print("\n========== TEST RESULT: FAILED ❌ ==========", flush=True)

    driver.quit()