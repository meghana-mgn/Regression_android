import sys
import time

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

TEST_PASSED = False

try:
    wait = WebDriverWait(driver, 20)

    # ==========================================================
    # Step 3 : Verify 3-dot menu button is visible
    # ==========================================================

    menu_btn = wait.until(
        EC.element_to_be_clickable(
            (
                AppiumBy.ID,
                "com.santa.web3.browser:id/menu_button"
            )
        )
    )

    assert menu_btn.is_displayed(), "3-dot menu button is not visible."

    print("Step 3: 3-dot menu button is visible.", flush=True)

    # ==========================================================
    # Step 4 : Click 3-dot menu
    # ==========================================================

    menu_btn.click()

    print("Step 4: 3-dot menu clicked successfully.", flush=True)

    time.sleep(2)

    # ==========================================================
    # Step 5 : Verify menu popup opened
    # ==========================================================

    menu_popup = wait.until(
        EC.visibility_of_element_located(
            (
                AppiumBy.XPATH,
                "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            )
        )
    )

    assert menu_popup.is_displayed(), "3-dot menu popup did not open."

    print("Step 5: 3-dot menu popup is visible.", flush=True)

    TEST_PASSED = True

except TimeoutException:
    print("TIMEOUT - Menu button or popup not found.", flush=True)
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