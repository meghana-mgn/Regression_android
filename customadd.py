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

# --------------------------------------------------
# Custom App Details
# --------------------------------------------------

APP_NAME = "ChatGPT"
APP_URL = "https://chatgpt.com"

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

    assert custom_tab.is_displayed(), "Custom tab not displayed."

    custom_tab.click()

    print("✅ Custom tab opened")

    # --------------------------------------------------
    # Locate both EditTexts
    # --------------------------------------------------

    edit_boxes = wait.until(
        EC.presence_of_all_elements_located((
            By.CLASS_NAME,
            "android.widget.EditText"
        ))
    )

    assert len(edit_boxes) >= 2, "Name/URL fields not found."

    app_name_box = edit_boxes[0]
    url_box = edit_boxes[1]

    # --------------------------------------------------
    # Enter App Name
    # --------------------------------------------------

    app_name_box.click()
    app_name_box.clear()
    app_name_box.send_keys(APP_NAME)

    print("✅ App name entered")

    # --------------------------------------------------
    # Enter URL
    # --------------------------------------------------

    url_box.click()
    url_box.clear()
    url_box.send_keys(APP_URL)

    print("✅ URL entered")

    # --------------------------------------------------
    # Click Add
    # --------------------------------------------------

    add_button = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//android.widget.Button[@text='Add']"
        ))
    )

    assert add_button.is_displayed(), "Add button not displayed."

    add_button.click()

    print("✅ Add button clicked")

    # --------------------------------------------------
    # Popup closes automatically
    # Wait for NTP
    # --------------------------------------------------

    ntp = wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            "//android.view.View[@resource-id='root']/android.view.View"
        ))
    )

    assert ntp.is_displayed(), "NTP not displayed."

    print("✅ Popup closed automatically")
    print("✅ NTP displayed")

    # --------------------------------------------------
    # Verify Custom App Added
    # --------------------------------------------------

    added_app = wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            f"//*[contains(@text,'{APP_NAME}') or contains(@content-desc,'{APP_NAME}')]"
        ))
    )

    assert added_app.is_displayed(), f"{APP_NAME} not added."

    print(f"✅ {APP_NAME} added successfully")

    print("\n========== TEST PASSED ==========")

except Exception as e:

    print("\n========== TEST FAILED ==========")
    print(e)

    # Helpful for debugging if verification fails
    print("\n========== PAGE SOURCE ==========\n")
    print(driver.page_source)

finally:
    driver.quit()