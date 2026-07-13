from appium import webdriver
from appium.options.android import UiAutomator2Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print("\n========== TEST STARTED ==========\n")

# --------------------------------------------------
# Desired Capabilities
# --------------------------------------------------

options = UiAutomator2Options()

options.platform_name = "Android"
options.device_name = "Android"
options.automation_name = "UiAutomator2"

options.app_package = "com.santa.web3.browser"
options.app_activity = "com.google.android.apps.chrome.Main"

# Keep app state
options.no_reset = True

driver = webdriver.Remote(
    "http://127.0.0.1:4723",
    options=options
)

wait = WebDriverWait(driver, 20)

try:

    # --------------------------------------------------
    # Click Custom tab
    # --------------------------------------------------

    custom_tab = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//*[@text='Custom']"
        ))
    )

    assert custom_tab.is_displayed(), "Custom tab is not displayed."

    custom_tab.click()

    print("✅ Custom tab opened")

    # --------------------------------------------------
    # Verify Cancel button
    # --------------------------------------------------

    cancel_button = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//android.widget.Button[@text='Cancel']"
        ))
    )

    assert cancel_button.is_displayed(), "Cancel button is not displayed."

    print("✅ Cancel button displayed")

    # --------------------------------------------------
    # Click Cancel
    # --------------------------------------------------

    cancel_button.click()

    print("✅ Cancel button clicked")

    # --------------------------------------------------
    # Verify NTP is displayed
    # --------------------------------------------------

    ntp = wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            "//android.view.View[@resource-id='root']/android.view.View"
        ))
    )

    assert ntp.is_displayed(), "NTP is not displayed after clicking Cancel."

    print("✅ NTP displayed")

    print("\n========== TEST PASSED ==========")

except Exception as e:

    print("\n========== TEST FAILED ==========")
    print(e)

finally:
    driver.quit()