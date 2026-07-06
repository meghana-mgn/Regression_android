import time

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
)

# ---------------------------------------------------
# Configuration
# ---------------------------------------------------

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

print("Launching Santa Browser...")

driver = webdriver.Remote(APPIUM_SERVER, options=options)

TEST_PASSED = False

try:
    wait = WebDriverWait(driver, 20)

    time.sleep(5)

    print("Current Package:", driver.current_package)

    # ---------------------------------------------------
    # If browser didn't launch, launch manually
    # ---------------------------------------------------

    if driver.current_package != PACKAGE_NAME:

        print("Santa Browser not launched automatically.")

        try:
            santa_icon = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (AppiumBy.ACCESSIBILITY_ID, "Santa")
                )
            )

            santa_icon.click()

            print("Clicked Santa app icon.")

            WebDriverWait(driver, 20).until(
                lambda d: d.current_package == PACKAGE_NAME
            )

        except Exception:
            raise AssertionError(
                "Unable to launch Santa Browser from launcher."
            )

    print("Santa Browser launched successfully.")

    # ---------------------------------------------------
    # Verify package
    # ---------------------------------------------------

    assert driver.current_package == PACKAGE_NAME, (
        f"Expected package '{PACKAGE_NAME}' "
        f"but found '{driver.current_package}'"
    )

    print("Package verification passed.")

    # ---------------------------------------------------
    # Verify NTP loaded
    # ---------------------------------------------------

    ntp = wait.until(
        EC.visibility_of_element_located(
            (
                AppiumBy.XPATH,
                '//android.view.View[@resource-id="root"]/android.view.View'
            )
        )
    )

    assert ntp.is_displayed(), "NTP page not visible."

    print("NTP is visible.")

    TEST_PASSED = True

except TimeoutException:

    print("\nTIMEOUT ERROR\n")
    print(driver.page_source)

except AssertionError as e:

    print("\nASSERTION FAILED:", e)
    print(driver.page_source)

except NoSuchElementException as e:

    print("\nELEMENT NOT FOUND:", e)
    print(driver.page_source)

except Exception as e:

    print("\nUNEXPECTED ERROR:", e)
    print(driver.page_source)

finally:

    if TEST_PASSED:
        print("\n========== TEST RESULT : PASSED ==========")
    else:
        print("\n========== TEST RESULT : FAILED ==========")

    driver.quit()