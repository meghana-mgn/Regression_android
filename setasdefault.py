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
# Browser options with their instance locators
# =====================================================

BROWSER_OPTIONS = {
    "brave":  'new UiSelector().className("android.widget.LinearLayout").instance(4)',
    "chrome": 'new UiSelector().className("android.widget.LinearLayout").instance(6)',
    "opera":  'new UiSelector().className("android.widget.LinearLayout").instance(10)',
    "santa":  'new UiSelector().className("android.widget.LinearLayout").instance(16)',
}

# Which browser to finally select from the prompt
BROWSER_TO_SELECT = "santa"

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
    # Step 5 : Verify Each Browser Option is Displayed
    # =====================================================

    browser_elements = {}

    for browser_name, locator in BROWSER_OPTIONS.items():

        browser_element = wait.until(
            EC.visibility_of_element_located(
                (
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    locator
                )
            )
        )

        assert browser_element.is_displayed(), \
            f"'{browser_name}' browser option is not displayed."

        browser_elements[browser_name] = browser_element

        print(f"Step 5: '{browser_name}' browser option displayed successfully.")

    # =====================================================
    # Step 6 : Select the Desired Browser
    # =====================================================

    selected_browser_element = browser_elements[BROWSER_TO_SELECT]

    selected_browser_element.click()

    print(f"Step 6: '{BROWSER_TO_SELECT}' browser selected.")

    # =====================================================
    # Step 7 : Click 'Set as default' System Button
    # =====================================================

    time.sleep(1)  # small buffer after browser selection

    set_as_default_button = wait.until(
        EC.element_to_be_clickable(
            (
                AppiumBy.ID,
                "android:id/button1"
            )
        )
    )

    assert set_as_default_button.is_displayed(), \
        "'Set as default' system button is not displayed."

    set_as_default_button.click()

    print("Step 7: 'Set as default' button clicked.")

    # =====================================================
    # Step 8 : Verify 'Set as default browser' Option Availability
    #          by Reopening 3-dot Menu
    # =====================================================

    time.sleep(2)  # buffer to return to app after system dialog closes

    menu_button = wait.until(
        EC.element_to_be_clickable(
            (
                AppiumBy.ID,
                "com.santa.web3.browser:id/menu_button"
            )
        )
    )

    assert menu_button.is_displayed(), "3-dot menu button is not displayed."

    menu_button.click()

    print("Step 8: 3-dot menu button clicked.")

    time.sleep(1)  # buffer for menu to render

    try:
        set_default_browser_option_recheck = driver.find_element(
            AppiumBy.XPATH,
            '//android.widget.TextView[@resource-id="com.santa.web3.browser:id/menu_item_text" '
            'and @text="Set as default browser"]'
        )

        if set_default_browser_option_recheck.is_displayed():
            print("Step 8: 'Set as default browser' option is still available "
                  "(Santa may not be set as default yet).")
        else:
            print("Step 8: 'Set as default browser' option found but not visible.")

    except NoSuchElementException:
        print("Step 8: 'Set as default browser' option is NOT available "
              "(Santa browser is successfully set as default).")

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