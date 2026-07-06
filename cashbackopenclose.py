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

    # --- Step 3: Click Cashback button ---
    cashback_btn = wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.ID, "com.santa.web3.browser:id/cashback_btn")
        )
    )
    cashback_btn.click()
    print("Step 4: Cashback button clicked.", flush=True)
    time.sleep(2)

    # ===== Assertion 1: Cashback popup is visible + content verified =====

    # 1a. Popup container visible
    popup_container = wait.until(
        EC.visibility_of_element_located(
            (AppiumBy.ID, "com.santa.web3.browser:id/tab_content")
        )
    )
    assert popup_container.is_displayed(), "Cashback popup container did not appear"

    # 1b. Cashback title visible
    cashback_title = wait.until(
        EC.visibility_of_element_located(
            (AppiumBy.XPATH, '//android.widget.TextView[@text="Cashback"]')
        )
    )
    assert cashback_title.is_displayed(), "Cashback popup title not visible"

    # 1c. Cashback balance visible
    cashback_balance = wait.until(
        EC.visibility_of_element_located(
            (AppiumBy.XPATH, '//android.widget.TextView[contains(@text, "$")]')
        )
    )
    assert cashback_balance.is_displayed(), "Cashback balance not visible"

    print(
        f"Step 5: Cashback popup opened. Title: 'Cashback', Balance: '{cashback_balance.text}'",
        flush=True,
    )

    # --- Step 6: Swipe DOWN on drag handle to close popup ---
    screen_height = driver.get_window_size()["height"]

    drag_handle_x = (424 + 655) // 2
    drag_handle_y = (141 + 228) // 2
    end_y = int(screen_height * 0.95)

    print(
        f"DEBUG - swipe from ({drag_handle_x}, {drag_handle_y}) to ({drag_handle_x}, {end_y})",
        flush=True,
    )

    driver.swipe(
        drag_handle_x,
        drag_handle_y,
        drag_handle_x,
        end_y,
        duration=800,
    )

    print("Step 7: Swiped down on drag handle to close cashback popup.", flush=True)
    time.sleep(2)

    # ===== Assertion 2: Cashback popup is NO LONGER visible =====
    popup_gone = wait.until(
        EC.invisibility_of_element_located(
            (AppiumBy.ID, "com.santa.web3.browser:id/tab_content")
        )
    )
    assert popup_gone, "Cashback popup is still visible after swipe"

    print("Step 8: Cashback popup closed successfully.", flush=True)

    # ===== Assertion 3: Verify NTP is visible =====
    ntp = wait.until(
        EC.visibility_of_element_located(
            (
                AppiumBy.XPATH,
                '//android.view.View[@resource-id="root"]/android.view.View'
            )
        )
    )

    assert ntp.is_displayed(), "NTP is not visible after closing cashback popup"

    print("Step 9: NTP is visible after closing cashback popup.", flush=True)

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
    print(driver.page_source)
    TEST_PASSED = False

finally:
    if TEST_PASSED:
        print("\n========== TEST RESULT: PASSED ✅ ==========", flush=True)
    else:
        print("\n========== TEST RESULT: FAILED ❌ ==========", flush=True)

    driver.quit()