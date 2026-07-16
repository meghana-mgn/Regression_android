import time

print("Step 1: Imports done", flush=True)

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException

print("Step 2: Creating Appium session...", flush=True)

# =====================================================
# Desired Capabilities
# =====================================================

options = UiAutomator2Options()

options.platform_name = "Android"
options.device_name = "Android Device"
options.automation_name = "UiAutomator2"

options.app_package = "com.santa.web3.browser"
options.app_activity = "com.google.android.apps.chrome.Main"

options.no_reset = True

driver = webdriver.Remote(
    "http://127.0.0.1:4723",
    options=options
)

wait = WebDriverWait(driver, 20)

TEST_PASSED = False

try:

    # =====================================================
    # Step 3 : Click Cashback button
    # =====================================================

    cashback_btn = wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.ID, "com.santa.web3.browser:id/cashback_btn")
        )
    )

    assert cashback_btn.is_displayed(), "Cashback button is not visible."

    cashback_btn.click()

    print("Step 3: Cashback button clicked.", flush=True)

    # =====================================================
    # Step 4 : Verify Cashback popup
    # =====================================================

    popup = wait.until(
        EC.visibility_of_element_located(
            (AppiumBy.ID, "com.santa.web3.browser:id/tab_content")
        )
    )

    assert popup.is_displayed(), "Cashback popup is not displayed."

    cashback_title = wait.until(
        EC.visibility_of_element_located(
            (
                AppiumBy.XPATH,
                '//android.widget.TextView[@text="Cashback"]'
            )
        )
    )

    cashback_balance = wait.until(
        EC.visibility_of_element_located(
            (
                AppiumBy.XPATH,
                '//android.widget.TextView[contains(@text,"$")]'
            )
        )
    )

    assert cashback_title.is_displayed()
    assert cashback_balance.is_displayed()

    print(
        f"Step 4: Cashback popup displayed. Balance: {cashback_balance.text}",
        flush=True
    )

    # =====================================================
    # Step 5 : Locate toolbar
    # =====================================================

    toolbar = wait.until(
        EC.visibility_of_element_located(
            (
                AppiumBy.ID,
                "com.santa.web3.browser:id/toolbar"
            )
        )
    )

    assert toolbar.is_displayed(), "Toolbar is not displayed."

    location = toolbar.location
    size = toolbar.size

    start_x = location["x"] + size["width"] // 2

    # Start well inside toolbar (avoids notification shade)
    start_y = location["y"] + (size["height"] // 2)

    end_y = start_y + 850

    print(
        f"Dragging toolbar from ({start_x}, {start_y}) "
        f"to ({start_x}, {end_y})",
        flush=True
    )

    # =====================================================
    # Step 6 : Drag toolbar down
    # =====================================================

    driver.execute_script(
        "mobile: dragGesture",
        {
            "startX": start_x,
            "startY": start_y,
            "endX": start_x,
            "endY": end_y,
            "speed": 6000
        }
    )

    print("Step 6: Drag gesture performed.", flush=True)

    time.sleep(2)

    # =====================================================
    # Step 7 : Verify popup closed
    # =====================================================

    popup_closed = wait.until(
        EC.invisibility_of_element_located(
            (
                AppiumBy.ID,
                "com.santa.web3.browser:id/tab_content"
            )
        )
    )

    assert popup_closed, "Cashback popup is still visible."

    print("Step 7: Cashback popup closed.", flush=True)

    # =====================================================
    # Step 8 : Verify NTP displayed
    # =====================================================

    ntp = wait.until(
        EC.visibility_of_element_located(
            (
                AppiumBy.XPATH,
                '//android.view.View[@resource-id="root"]/android.view.View'
            )
        )
    )

    assert ntp.is_displayed(), "NTP is not visible."

    print("Step 8: NTP is visible.", flush=True)

    TEST_PASSED = True

except TimeoutException:

    print("\nTIMEOUT OCCURRED\n", flush=True)
    print(driver.page_source)

except AssertionError as e:

    print(f"\nASSERTION FAILED: {e}\n", flush=True)
    print(driver.page_source)

except Exception as e:

    print(f"\nUNEXPECTED ERROR: {e}\n", flush=True)
    print(driver.page_source)

finally:

    if TEST_PASSED:
        print("\n========== TEST RESULT : PASSED ==========\n")
    else:
        print("\n========== TEST RESULT : FAILED ==========\n")

    driver.quit()