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

try:

    # =====================================================
    # Step 1 : Click 'Set as default browser' Menu Option
    # =====================================================

    set_default_browser_option = wait.until(
        EC.element_to_be_clickable(
            (
                AppiumBy.XPATH,
                '//android.widget.TextView[@resource-id="com.santa.web3.browser:id/menu_item_text" '
                'and @text="Set as default browser"]'
            )
        )
    )

    assert set_default_browser_option.is_displayed(), \
        "'Set as default browser' option is not displayed."

    set_default_browser_option.click()

    print("Step 1: 'Set as default browser' option clicked.")

    # =====================================================
    # Step 2 : Verify Prompt Displayed
    # =====================================================

    time.sleep(2)  # buffer for system prompt/dialog to render

    default_browser_prompt = wait.until(
        EC.visibility_of_element_located(
            (
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().className("android.widget.LinearLayout").instance(1)'
            )
        )
    )

    assert default_browser_prompt.is_displayed(), \
        "Set as default browser prompt did not appear."

    print("Step 2: Set as default browser prompt displayed successfully.")

    # =====================================================
    # Step 3 : Click 'Next' Button
    # =====================================================

    next_button = wait.until(
        EC.element_to_be_clickable(
            (
                AppiumBy.ID,
                "com.santa.web3.browser:id/btn_next"
            )
        )
    )

    assert next_button.is_displayed(), "'Next' button is not displayed."

    next_button.click()

    print("Step 3: 'Next' button clicked.")

    # =====================================================
    # Step 4 : Verify Browser Options Prompt Displayed
    # =====================================================

    time.sleep(2)  # buffer for system browser-chooser dialog to render

    browser_options_prompt = wait.until(
        EC.visibility_of_element_located(
            (
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().className("android.widget.LinearLayout").instance(2)'
            )
        )
    )

    assert browser_options_prompt.is_displayed(), \
        "Browser options prompt did not appear."

    print("Step 4: Browser options prompt displayed successfully.")

    # =====================================================
    # Step 5 : Click 'Cancel' Button (System Dialog - button2)
    # =====================================================

    cancel_button = wait.until(
        EC.element_to_be_clickable(
            (
                AppiumBy.ID,
                "android:id/button2"
            )
        )
    )

    assert cancel_button.is_displayed(), "'Cancel' (button2) is not displayed."

    cancel_button.click()

    print("Step 5: 'Cancel' button (button2) clicked.")

    # =====================================================
    # Step 6 : Verify Browser Options Prompt Closed
    # =====================================================

    time.sleep(1)

    prompt_closed = False
    try:
        wait_short = WebDriverWait(driver, 5)
        wait_short.until(
            EC.invisibility_of_element_located(
                (
                    AppiumBy.ID,
                    "android:id/button2"
                )
            )
        )
        prompt_closed = True
    except TimeoutException:
        prompt_closed = False

    assert prompt_closed, "Browser options prompt did not close after clicking Cancel."

    print("Step 6: Browser options prompt closed successfully.")

    # =====================================================
    # Step 7 : Verify NTP (New Tab Page) is Visible
    # =====================================================

    ntp_element = wait.until(
        EC.visibility_of_element_located(
            (
                AppiumBy.ID,
                "com.santa.web3.browser:id/ntp_overlay"
            )
        )
    )

    assert ntp_element.is_displayed(), "NTP is not displayed."

    print("Step 7: NTP is displayed successfully.")

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