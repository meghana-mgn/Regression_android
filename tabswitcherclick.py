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

TAB_SWITCHER_BUTTON_ID = "com.santa.web3.browser:id/tab_switcher_button"
TAB_LIST_RECYCLER_VIEW_ID = "com.santa.web3.browser:id/tab_list_recycler_view"

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

    # Step 3: Verify tab switcher button is visible and clickable.
    tab_switcher_button = wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.ID, TAB_SWITCHER_BUTTON_ID)
        )
    )

    assert tab_switcher_button.is_displayed(), "Tab switcher button is not visible."
    print("Step 3: Tab switcher button is visible.", flush=True)

    # Step 4: Click tab switcher button.
    tab_switcher_button.click()
    print("Step 4: Tab switcher button clicked successfully.", flush=True)
    time.sleep(2)

    # Step 5: Verify tab list recycler view is visible.
    tab_list_recycler_view = wait.until(
        EC.visibility_of_element_located(
            (AppiumBy.ID, TAB_LIST_RECYCLER_VIEW_ID)
        )
    )

    assert tab_list_recycler_view.is_displayed(), "Tab list recycler view is not visible."
    print("Step 5: Tab list recycler view is visible.", flush=True)

    TEST_PASSED = True

except TimeoutException:
    print("TIMEOUT - Tab switcher button or tab list recycler view not found.", flush=True)
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
        print("\n========== TEST RESULT: PASSED ==========", flush=True)
    else:
        print("\n========== TEST RESULT: FAILED ==========", flush=True)

    driver.quit()
