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

    # ===== Assertion 1: Santa Browser is open and running =====
    browser_root = wait.until(
        EC.visibility_of_element_located(
            (AppiumBy.ID, "com.santa.web3.browser:id/cashback_btn")
        )
    )
    assert browser_root.is_displayed(), "Santa Browser did not launch correctly"
    print("Step 3: Santa Browser is open and running.", flush=True)

    # --- Step 4: Open Recents/App Switcher ---
    driver.press_keycode(187)
    print("Step 4: Opened Recents screen.", flush=True)
    time.sleep(2)

    # --- Step 5: Swipe app card UP to remove it from Recents ---
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

    # --- Step 6: Reopen Santa Browser ---
    driver.activate_app(PACKAGE_NAME)
    print("Step 6: Santa Browser reopened.", flush=True)
    time.sleep(2)

    # ===== Assertion 2: Santa Browser relaunched successfully =====
    browser_root = wait.until(
        EC.visibility_of_element_located(
            (AppiumBy.ID, "com.santa.web3.browser:id/cashback_btn")
        )
    )
    assert browser_root.is_displayed(), "Santa Browser did not relaunch after removing from Recents"
    print("Step 7: Santa Browser relaunched successfully.", flush=True)

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