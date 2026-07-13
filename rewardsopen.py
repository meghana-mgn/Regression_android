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

TEST_PASSED = False

try:
    wait = WebDriverWait(driver, 20)

    # ==========================================================
    # Step 3 : Click Rewards button
    # ==========================================================

    rewards_btn = wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.ID, "com.santa.web3.browser:id/rewards_btn")
        )
    )

    assert rewards_btn.is_displayed(), "Rewards button is not visible."

    rewards_btn.click()

    print("Step 3: Rewards button clicked successfully.", flush=True)

    time.sleep(3)

    # ==========================================================
    # Step 4 : Verify Rewards page is opened
    # ==========================================================

    rewards_page = wait.until(
        EC.visibility_of_element_located(
            (
                AppiumBy.XPATH,
                '//android.webkit.WebView[@text="Santa Rewards"]/android.view.View/android.view.View/android.view.View[1]/android.view.View'
            )
        )
    )

    assert rewards_page.is_displayed(), "Rewards page did not open."

    print("Step 4: Rewards page is visible.", flush=True)

    # ==========================================================
    # Step 5 : Verify '+' button is visible
    # ==========================================================

    plus_btn = wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.ID, "com.santa.web3.browser:id/optional_toolbar_button")
        )
    )

    assert plus_btn.is_displayed(), "'+' button is not visible."

    print("Step 5: '+' button is visible.", flush=True)

    # ==========================================================
    # Step 6 : Click '+' button
    # ==========================================================

    plus_btn.click()

    print("Step 6: '+' button clicked successfully.", flush=True)

    time.sleep(3)

    # ==========================================================
    # Step 7 : Verify NTP is visible
    # ==========================================================

    ntp = wait.until(
        EC.visibility_of_element_located(
            (
                AppiumBy.XPATH,
                '//android.view.View[@resource-id="root"]/android.view.View'
            )
        )
    )

    assert ntp.is_displayed(), "NTP is not visible after returning from Rewards page."

    print("Step 7: NTP is visible.", flush=True)

    # ==========================================================
    # Step 8 : Verify Rewards button is visible again on NTP
    # ==========================================================

    rewards_btn = wait.until(
        EC.visibility_of_element_located(
            (AppiumBy.ID, "com.santa.web3.browser:id/rewards_btn")
        )
    )

    assert rewards_btn.is_displayed(), "Rewards button is not visible on NTP."

    print("Step 8: Rewards button is visible on NTP.", flush=True)

    TEST_PASSED = True

except TimeoutException:
    print("TIMEOUT - dumping current page source for inspection", flush=True)
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