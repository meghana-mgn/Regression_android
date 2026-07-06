import sys
import time

print("Step 1: imports done", flush=True)

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

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
    time.sleep(2)

    # ==========================================================
    # Step 3 : Click Playwall button
    # ==========================================================
    playwall_btn = wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.ID, "com.santa.web3.browser:id/playwall_btn")
        )
    )

    playwall_btn.click()
    print("Step 3: Playwall button clicked.", flush=True)

    time.sleep(3)

    # ==========================================================
    # Step 4 : Verify Playwall popup opened
    # ==========================================================
    popup_container = wait.until(
        EC.visibility_of_element_located(
            (AppiumBy.ID, "com.santa.web3.browser:id/tab_content")
        )
    )

    assert popup_container.is_displayed(), "Playwall popup did not appear"

    # ==========================================================
    # Get Playwall Title
    # ==========================================================
    try:
        playwall_title = driver.find_element(
            AppiumBy.XPATH,
            "//*[contains(@text,'Playwall') or contains(@text,'Earn')]"
        )

        title_text = playwall_title.text.strip()

        # Remove "| SantaBrowser"
        title_text = title_text.replace("| SantaBrowser", "").strip()

    except NoSuchElementException:
        title_text = "Playwall"

    # ==========================================================
    # Get first amount displayed
    # ==========================================================
    balance_text = "Not Found"

    try:
        amount_elements = driver.find_elements(
            AppiumBy.XPATH,
            "//*[contains(@text,'$')]"
        )

        for element in amount_elements:
            value = element.text.strip()

            if value.startswith("$"):
                balance_text = value
                break

    except Exception:
        balance_text = "Not Found"

    print(
        f"Step 4: Playwall popup opened.\n"
        f"Title   : {title_text}\n"
        f"Balance : {balance_text}",
        flush=True
    )

    # ==========================================================
    # Step 5 : Swipe down to close Playwall
    # ==========================================================
    toolbar = wait.until(
        EC.presence_of_element_located(
            (AppiumBy.ID, "com.santa.web3.browser:id/toolbar")
        )
    )

    loc = toolbar.location
    size = toolbar.size

    start_x = loc["x"] + size["width"] // 2
    start_y = loc["y"] + size["height"] // 2
    end_y = start_y + 800

    print(
        f"DEBUG - swipe from ({start_x}, {start_y}) to ({start_x}, {end_y})",
        flush=True
    )

    driver.swipe(start_x, start_y, start_x, end_y, 800)

    print("Step 5: Swiped down on drag handle to close Playwall.", flush=True)

    time.sleep(2)

    # ==========================================================
    # Step 6 : Verify popup closed
    # ==========================================================
    popup_closed = wait.until(
        EC.invisibility_of_element_located(
            (AppiumBy.ID, "com.santa.web3.browser:id/tab_content")
        )
    )

    assert popup_closed, "Playwall popup still visible"

    print("Step 6: Playwall popup closed successfully.", flush=True)

    # ==========================================================
    # Step 7 : Verify NTP visible
    # ==========================================================
    ntp = wait.until(
        EC.visibility_of_element_located(
            (
                AppiumBy.XPATH,
                '//android.view.View[@resource-id="root"]/android.view.View'
            )
        )
    )

    assert ntp.is_displayed(), "NTP not visible after closing Playwall"

    print("Step 7: NTP is visible after closing Playwall.", flush=True)

    TEST_PASSED = True

except TimeoutException:
    print("\nTIMEOUT - dumping page source\n", flush=True)
    print(driver.page_source)
    TEST_PASSED = False

except AssertionError as e:
    print(f"\nASSERTION FAILED: {e}", flush=True)
    print(driver.page_source)
    TEST_PASSED = False

except Exception as e:
    print(f"\nUNEXPECTED ERROR: {e}", flush=True)
    print(driver.page_source)
    TEST_PASSED = False

finally:
    if TEST_PASSED:
        print("\n========== TEST RESULT: PASSED ==========\n", flush=True)
    else:
        print("\n========== TEST RESULT: FAILED ==========\n", flush=True)

    driver.quit()