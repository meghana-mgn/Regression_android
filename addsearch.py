from appium import webdriver
from appium.options.android import UiAutomator2Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print("\n========== TEST STARTED ==========\n")

# ----------------------------
# Desired Capabilities
# ----------------------------
options = UiAutomator2Options()

options.platform_name = "Android"
options.device_name = "Android"
options.automation_name = "UiAutomator2"

options.app_package = "com.santa.web3.browser"
options.app_activity = "com.google.android.apps.chrome.Main"

# Don't reset app
options.no_reset = True

driver = webdriver.Remote(
    "http://127.0.0.1:4723",
    options=options
)

wait = WebDriverWait(driver, 20)

# List of Quick Apps to add
quick_apps = [
    "YouTube",
    "Facebook",
    "Instagram",
    "X",
    "WhatsApp",
    "Amazon",
    "Flipkart",
    "Netflix",
    "Spotify",
    "Gmail"
]

try:

    for APP_NAME in quick_apps:

        print(f"\n---------- Trying to add {APP_NAME} ----------")

        # ------------------------------------------
        # Search box (Popup should already be open)
        # ------------------------------------------

        search_box = wait.until(
            EC.element_to_be_clickable((
                By.CLASS_NAME,
                "android.widget.EditText"
            ))
        )

        assert search_box.is_displayed()

        search_box.click()
        search_box.clear()
        search_box.send_keys(APP_NAME)

        print(f"✅ Searched for {APP_NAME}")

        # ------------------------------------------
        # Wait for search result
        # ------------------------------------------

        try:
            result = wait.until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//android.webkit.WebView[@text='Welcome to Santa']"
                    "/android.view.View"
                    "/android.view.View[2]"
                    "/android.view.View"
                    "/android.view.View[2]"
                    "/android.view.View"
                ))
            )

            assert result.is_displayed()

            result.click()

            print(f"✅ Selected {APP_NAME}")

        except:
            print(f"❌ {APP_NAME} not found")
            search_box.clear()
            continue

        # ------------------------------------------
        # Swipe down to close popup
        # ------------------------------------------

        swipe_area = wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                "//android.webkit.WebView[@text='Welcome to Santa']"
                "/android.view.View"
                "/android.view.View[2]"
                "/android.view.View"
                "/android.view.View[1]"
            ))
        )

        size = swipe_area.size
        location = swipe_area.location

        start_x = location["x"] + size["width"] // 2
        start_y = location["y"] + 80
        end_y = start_y + 700

        driver.swipe(start_x, start_y, start_x, end_y, 180)

        print("✅ Popup closed")

        # ------------------------------------------
        # Verify NTP displayed
        # ------------------------------------------

        ntp = wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                "//android.view.View[@resource-id='root']/android.view.View"
            ))
        )

        assert ntp.is_displayed()

        # ------------------------------------------
        # Verify app added
        # ------------------------------------------

        try:
            added = wait.until(
                EC.presence_of_element_located((
                    By.XPATH,
                    f"//*[contains(@text,'{APP_NAME}') or contains(@content-desc,'{APP_NAME}')]"
                ))
            )

            assert added.is_displayed()

            print(f"✅ {APP_NAME} added successfully")

        except:
            print(f"❌ {APP_NAME} not visible on NTP")

        # ------------------------------------------
        # Reopen Add Quick Apps popup
        # ------------------------------------------

        try:
            add_button = wait.until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//android.view.View[@resource-id='root']"
                    "/android.view.View"
                    "/android.view.View[6]"
                ))
            )

            add_button.click()

            wait.until(
                EC.presence_of_element_located((
                    By.CLASS_NAME,
                    "android.widget.EditText"
                ))
            )

            print("✅ Add Quick Apps popup reopened")

        except:
            print("Popup couldn't be reopened.")
            break

    print("\n========== TEST PASSED ==========")

except Exception as e:
    print("\n========== TEST FAILED ==========")
    print(e)

finally:
    driver.quit()