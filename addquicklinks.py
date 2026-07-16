from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException
import time

print("\n========== TEST STARTED ==========\n")

# ---------------------------------------------------
# Desired Capabilities
# ---------------------------------------------------

options = UiAutomator2Options()

options.platform_name = "Android"
options.device_name = "Android"
options.automation_name = "UiAutomator2"

options.app_package = "com.santa.web3.browser"
options.app_activity = "com.google.android.apps.chrome.Main"

# Don't clear app data
options.no_reset = True

driver = webdriver.Remote(
    "http://127.0.0.1:4723",
    options=options
)

wait = WebDriverWait(driver, 30)

try:

    # ---------------------------------------------------
    # Step 1 : Verify Add (+) button
    # ---------------------------------------------------

    add_btn = wait.until(
        EC.element_to_be_clickable((
            AppiumBy.XPATH,
            '//android.view.View[@resource-id="root"]/android.view.View/android.view.View[6]/android.widget.Image'
        ))
    )

    assert add_btn.is_displayed(), "Add (+) button is not displayed."

    print("PASS - Add (+) button displayed.")

    # ---------------------------------------------------
    # Step 2 : Click Add (+) button
    # ---------------------------------------------------

    add_btn.click()

    print("PASS - Add (+) button clicked.")

    # ---------------------------------------------------
    # Step 3 : Verify All & Custom tabs
    # ---------------------------------------------------

    all_tab = wait.until(
        EC.visibility_of_element_located((
            AppiumBy.XPATH,
            '//*[@text="All"]'
        ))
    )

    custom_tab = wait.until(
        EC.visibility_of_element_located((
            AppiumBy.XPATH,
            '//*[@text="Custom"]'
        ))
    )

    assert all_tab.is_displayed(), "'All' tab is not displayed."
    assert custom_tab.is_displayed(), "'Custom' tab is not displayed."

    print("PASS - Quick Apps popup opened with All & Custom tabs.")

    time.sleep(1)

    # ---------------------------------------------------
    # Step 4 : Swipe down to close Quick Apps popup
    # ---------------------------------------------------

    swipe_area = wait.until(
        EC.presence_of_element_located((
            AppiumBy.XPATH,
            '//android.webkit.WebView[@text="Welcome to Santa"]/android.view.View/android.view.View[2]/android.view.View/android.view.View[1]'
        ))
    )

    assert swipe_area.is_displayed(), "Swipe area not found."

    location = swipe_area.location
    size = swipe_area.size

    start_x = location["x"] + size["width"] // 2
    start_y = location["y"] + 100
    end_y = start_y + 900

    # Swipe down quickly
    driver.swipe(start_x, start_y, start_x, end_y, 150)

    print("PASS - Quick Apps popup closed.")

    time.sleep(2)

    # ---------------------------------------------------
    # Step 5 : Verify NTP is displayed
    # ---------------------------------------------------

    ntp = wait.until(
        EC.presence_of_element_located((
            AppiumBy.XPATH,
            '//android.webkit.WebView[@text="Welcome to Santa"]'
        ))
    )

    assert ntp.is_displayed(), "NTP is not displayed."

    print("PASS - NTP is displayed.")

    print("\n========== TEST PASSED ==========")

except TimeoutException:
    print("\n========== TEST FAILED ==========")
    print("Timeout: Element not found within 30 seconds.")
    print(driver.page_source)

except AssertionError as ae:
    print("\n========== TEST FAILED ==========")
    print("Assertion Error:", ae)

except Exception as e:
    print("\n========== TEST FAILED ==========")
    print("Exception:", e)
    print(driver.page_source)

finally:
    driver.quit()