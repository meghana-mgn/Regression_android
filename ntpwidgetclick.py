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

TEST_PASSED = False  # overall result flag

try:
    wait = WebDriverWait(driver, 15)
    time.sleep(2)

    # --- Step 3: Click Santa Points / Cash Rewards ---
    santa_points = wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.XPATH, '//android.view.View[@content-desc="Open rewards"]')
        )
    )
    santa_points.click()
    print("Step 4: Santa Points / Cash Rewards clicked.", flush=True)
    time.sleep(2)

    # ===== Assertion 1: Rewards page opened =====
    rewards_page = wait.until(
        EC.visibility_of_element_located(
            (AppiumBy.ID, "com.santa.web3.browser:id/optional_toolbar_button")
        )
    )
    assert rewards_page.is_displayed(), "Rewards page did not open"
    print("Step 5: Rewards page opened successfully.", flush=True)

    # --- Step 6: Click '+' to return to NTP ---
    plus_btn = wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.ID, "com.santa.web3.browser:id/optional_toolbar_button")
        )
    )
    plus_btn.click()
    print("Step 7: '+' button clicked to return to NTP.", flush=True)
    time.sleep(2)

    # ===== Assertion 2: Back on NTP - Santa Points button visible =====
    santa_points = wait.until(
        EC.visibility_of_element_located(
            (AppiumBy.XPATH, '//android.view.View[@content-desc="Open rewards"]')
        )
    )
    assert santa_points.is_displayed(), "Did not return to NTP after clicking '+'"
    print("Step 8: Returned to NTP successfully.", flush=True)

    TEST_PASSED = True

except TimeoutException:
    print("TIMEOUT - dumping page source for inspection", flush=True)
    print(driver.page_source)
    TEST_PASSED = False

except AssertionError as e:
    print(f"ASSERTION FAILED: {e}", flush=True)
    print(driver.page_source)
    TEST_PASSED = False

except Exception as e:
    print(f"UNEXPECTED ERROR: {e}", flush=True)
    TEST_PASSED = False

finally:
    if TEST_PASSED:
        print("\n========== TEST RESULT: PASSED ✅ ==========", flush=True)
    else:
        print("\n========== TEST RESULT: FAILED ❌ ==========", flush=True)
    driver.quit()