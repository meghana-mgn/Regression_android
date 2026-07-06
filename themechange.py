from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

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
wait = WebDriverWait(driver, 20)

THEME_BUTTON = "com.santa.web3.browser:id/theme_btn"


def get_theme():
    """
    Detect current theme using the Theme button state.
    selected = true  -> Dark (Sun icon)
    selected = false -> Light (Moon icon)
    """

    btn = driver.find_element(AppiumBy.ID, THEME_BUTTON)

    selected = btn.get_attribute("selected")
    checked = btn.get_attribute("checked")
    desc = btn.get_attribute("contentDescription") or btn.get_attribute("content-desc") or ""

    print("\n----- Theme Button Attributes -----")
    print("selected :", selected)
    print("checked  :", checked)
    print("content-desc :", desc)
    print("-----------------------------------")

    if selected == "true" or checked == "true":
        return "Dark (Sun Icon)"
    else:
        return "Light (Moon Icon)"


try:

    before = get_theme()
    print(f"\nCurrent Theme : {before}")

    theme_btn = wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.ID, THEME_BUTTON)
        )
    )

    theme_btn.click()
    print("Theme button clicked.")

    time.sleep(2)

    after = get_theme()
    print(f"Theme After : {after}")

    print("\n========== RESULT ==========")

    if before != after:
        print("✅ PASS")
        print(f"Theme changed successfully: {before} → {after}")
    else:
        print("❌ FAIL")
        print("Theme did not change.")

except TimeoutException:
    print("❌ Theme button not found.")

finally:
    driver.quit()