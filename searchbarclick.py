import sys
import time

print("Step 1: imports done", flush=True)

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException
)

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

    # =====================================================
    # Step 3 : Click Search Bar
    # =====================================================

    search_box = wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.ID, "com.santa.web3.browser:id/search_box_text")
        )
    )

    assert search_box.is_displayed(), "Search bar is not visible."

    search_box.click()

    print("Step 3: Search bar clicked successfully.", flush=True)

    # =====================================================
    # Step 4 : Verify Keyboard Opened
    # =====================================================

    time.sleep(2)

    url_bar = wait.until(
        EC.visibility_of_element_located(
            (AppiumBy.ID, "com.santa.web3.browser:id/url_bar")
        )
    )

    assert url_bar.is_displayed(), "URL bar is not visible."

    focused = url_bar.get_attribute("focused")

    assert focused == "true", "Keyboard did not open (URL bar is not focused)."

    print("Step 4: Keyboard is displayed.", flush=True)

    # =====================================================
    # Step 5 : Enter Search Text
    # =====================================================

    url_bar.clear()
    url_bar.send_keys("hello")

    print("Step 5: Typed 'hello' successfully.", flush=True)

    time.sleep(2)

    # =====================================================
    # Step 6 : Verify Autosuggestions
    # =====================================================

    suggestion_list = wait.until(
        EC.visibility_of_element_located(
            (
                AppiumBy.XPATH,
                '//androidx.recyclerview.widget.RecyclerView[contains(@content-desc,"suggested items")]'
            )
        )
    )

    assert suggestion_list.is_displayed(), \
        "Autosuggestions are not visible."

    print("Step 6: Autosuggestions are visible.", flush=True)

    # =====================================================
    # Step 7 : Click First Autosuggestion
    # =====================================================

    first_suggestion = wait.until(
        EC.element_to_be_clickable(
            (
                AppiumBy.XPATH,
                '//androidx.recyclerview.widget.RecyclerView[contains(@content-desc,"suggested items")]/android.view.ViewGroup[1]'
            )
        )
    )

    assert first_suggestion.is_displayed(), \
        "First autosuggestion is not visible."

    first_suggestion.click()

    print("Step 7: First autosuggestion clicked.", flush=True)

    # =====================================================
    # Step 8 : Verify Landing Page
    # =====================================================

    time.sleep(5)

    url_bar = wait.until(
        EC.visibility_of_element_located(
            (AppiumBy.ID, "com.santa.web3.browser:id/url_bar")
        )
    )

    current_page = url_bar.text.strip()

    assert current_page != "", "Landing page did not load."

    print("Step 8: Landing page loaded successfully.", flush=True)
    print(f"Current URL/Page: {current_page}", flush=True)

    TEST_PASSED = True

# =====================================================
# Exception Handling
# =====================================================

except TimeoutException:

    print("\nTIMEOUT OCCURRED\n", flush=True)
    print(driver.page_source)

except AssertionError as e:

    print(f"\nASSERTION FAILED: {e}\n", flush=True)
    print(driver.page_source)

except NoSuchElementException:

    print("\nELEMENT NOT FOUND\n", flush=True)
    print(driver.page_source)

except Exception as e:

    print(f"\nUNEXPECTED ERROR: {e}\n", flush=True)
    print(driver.page_source)

# =====================================================
# Final Result
# =====================================================

finally:

    if TEST_PASSED:
        print("\n========== TEST RESULT : PASSED ==========\n")
    else:
        print("\n========== TEST RESULT : FAILED ==========\n")

    driver.quit()