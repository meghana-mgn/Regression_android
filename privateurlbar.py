import time

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException
)

print("\n========== TEST STARTED ==========\n")

# =====================================================
# Desired Capabilities
# =====================================================

PACKAGE_NAME = "com.santa.web3.browser"
APP_ACTIVITY = "com.google.android.apps.chrome.Main"
APPIUM_SERVER = "http://127.0.0.1:4723"

options = UiAutomator2Options()
options.platform_name = "Android"
options.device_name = "Android Device"
options.automation_name = "UiAutomator2"

options.app_package = PACKAGE_NAME
options.app_activity = APP_ACTIVITY

# Don't clear app data
options.no_reset = True

driver = webdriver.Remote(
    APPIUM_SERVER,
    options=options
)

wait = WebDriverWait(driver, 30)

TEST_PASSED = False

# =====================================================
# Keyword to search
# =====================================================

SEARCH_KEYWORD = "python appium"

try:

    # =====================================================
    # Step 1 : Click on URL Bar
    # =====================================================

    url_bar = wait.until(
        EC.element_to_be_clickable(
            (
                AppiumBy.ID,
                "com.santa.web3.browser:id/url_bar"
            )
        )
    )

    assert url_bar.is_displayed(), "URL bar is not displayed."

    url_bar.click()

    print("Step 1: URL bar clicked.")

    # =====================================================
    # Step 2 : Verify Keyboard Opened (URL bar focused)
    # =====================================================

    time.sleep(1)  # small buffer for focus state to update

    url_bar = wait.until(
        EC.visibility_of_element_located(
            (
                AppiumBy.ID,
                "com.santa.web3.browser:id/url_bar"
            )
        )
    )

    is_focused = url_bar.get_attribute("focused")
    print("URL bar focused attribute:", is_focused)

    assert is_focused == "true", "Keyboard did not open / URL bar not focused."

    print("Step 2: Keyboard displayed.")

    # =====================================================
    # Step 3 : Enter Search Keyword
    # =====================================================

    url_bar.clear()
    url_bar.send_keys(SEARCH_KEYWORD)

    print(f"Step 3: Entered keyword '{SEARCH_KEYWORD}'.")

    # =====================================================
    # Step 4 : Verify Entered Text in URL Bar
    # =====================================================

    entered_text = url_bar.text.strip()
    print("Text currently in URL bar:", entered_text)

    assert entered_text == SEARCH_KEYWORD, \
        f"Entered text mismatch. Expected '{SEARCH_KEYWORD}', got '{entered_text}'."

    print("Step 4: Verified keyword present in URL bar.")

    # =====================================================
    # Step 5 : Press Enter to submit search
    # =====================================================

    driver.press_keycode(66)  # 66 = Android KEYCODE_ENTER

    print("Step 5: Search submitted.")

    # =====================================================
    # Step 6 : Verify Page/Results Loaded
    # =====================================================

    time.sleep(5)

    url_bar = wait.until(
        EC.visibility_of_element_located(
            (
                AppiumBy.ID,
                "com.santa.web3.browser:id/url_bar"
            )
        )
    )

    current_url = url_bar.text.strip()
    print("Current URL bar text:", current_url)

    assert current_url != "", "Search results / page not loaded."

    print("Step 6: Search results loaded.")

    # =====================================================
    # Step 7 : Click '+' Button to Open New Private Tab
    # =====================================================

    plus_button = wait.until(
        EC.element_to_be_clickable(
            (
                AppiumBy.ID,
                "com.santa.web3.browser:id/optional_toolbar_button"
            )
        )
    )

    assert plus_button.is_displayed(), "'+' button is not displayed."

    plus_button.click()

    print("Step 7: '+' button clicked.")

    # =====================================================
    # Step 8 : Verify New Private Tab Opened
    # =====================================================

    incognito_container = wait.until(
        EC.visibility_of_element_located(
            (
                AppiumBy.ID,
                "com.santa.web3.browser:id/new_tab_incognito_container"
            )
        )
    )

    assert incognito_container.is_displayed(), \
        "New private tab did not open (incognito container not visible)."

    print("Step 8: New private tab opened successfully.")

    TEST_PASSED = True

# =====================================================
# Exception Handling
# =====================================================

except TimeoutException:
    print("\n========== TEST FAILED ==========")
    print("Timeout occurred.")
    print(driver.page_source)

except AssertionError as e:
    print("\n========== TEST FAILED ==========")
    print("Assertion Error:", e)
    print(driver.page_source)

except NoSuchElementException:
    print("\n========== TEST FAILED ==========")
    print("Element not found.")
    print(driver.page_source)

except Exception as e:
    print("\n========== TEST FAILED ==========")
    print(e)
    print(driver.page_source)

# =====================================================
# Close Driver
# =====================================================

finally:

    if TEST_PASSED:
        print("\n========== TEST PASSED ==========\n")
    else:
        print("\n========== TEST FAILED ==========\n")

    driver.quit()