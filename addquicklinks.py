from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ---------------- Desired Capabilities ----------------

options = UiAutomator2Options()
options.platform_name = "Android"
options.device_name = "Android"
options.automation_name = "UiAutomator2"
options.app_package = "com.santa.web3.browser"
options.app_activity = "com.santa.web3.browser.MainActivity"
options.no_reset = True

# ---------------- Start Driver ----------------

driver = webdriver.Remote(
    "http://127.0.0.1:4723",
    options=options
)

wait = WebDriverWait(driver, 20)

try:

    # Step 1 - Verify Add (+) button
    add_btn = wait.until(
        EC.presence_of_element_located((
            AppiumBy.XPATH,
            '//android.view.View[@resource-id="root"]/android.view.View/android.view.View[6]'
        ))
    )

    assert add_btn.is_displayed(), "Add (+) button is not displayed."
    print("PASS - Add (+) button located.")

    # Step 2 - Click Add button
    add_btn.click()
    print("PASS - Quick Apps panel opened.")

    time.sleep(2)

    # Step 3 - Verify All & Custom options
    all_tab = wait.until(
        EC.presence_of_element_located((
            AppiumBy.XPATH,
            '//*[@text="All"]'
        ))
    )

    custom_tab = wait.until(
        EC.presence_of_element_located((
            AppiumBy.XPATH,
            '//*[@text="Custom"]'
        ))
    )

    assert all_tab.is_displayed() and custom_tab.is_displayed(), \
        "'All' and/or 'Custom' option not displayed."

    print("PASS - Quick Apps panel displays 'All' and 'Custom' options.")

    time.sleep(1)

    # Step 4 - Drag down to close Quick Apps
    driver.execute_script(
        "mobile: dragGesture",
        {
            "startX": 540,
            "startY": 700,
            "endX": 540,
            "endY": 1900,
            "speed": 8000
        }
    )

    print("PASS - Dragged down to close Quick Apps.")

    time.sleep(2)

    # Step 5 - Verify NTP
    ntp = wait.until(
        EC.presence_of_element_located((
            AppiumBy.XPATH,
            '//android.webkit.WebView[@text="Welcome to Santa"]'
        ))
    )

    assert ntp.is_displayed(), "NTP is not displayed."

    print("PASS - NTP is displayed.")

    print("\n========== TEST PASSED ==========")

except AssertionError as ae:
    print("\n========== TEST FAILED ==========")
    print("Assertion Error:", ae)

except Exception as e:
    print("\n========== TEST FAILED ==========")
    print("Exception:", e)
    print(driver.page_source)

finally:
    driver.quit()