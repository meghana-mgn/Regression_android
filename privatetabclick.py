import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_open_new_private_tab():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "Android Device"
    options.app_package = "com.santa.web3.browser"
    options.app_activity = "com.santa.web3.browser.MainActivity"
    options.automation_name = "UiAutomator2"
    options.no_reset = True

    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    wait = WebDriverWait(driver, 15)

    try:
        # Step 1: Click on "New private tab"
        new_private_tab_locator = (AppiumBy.ID, "com.santa.web3.browser:id/title")
        new_private_tab_element = wait.until(
            EC.element_to_be_clickable(new_private_tab_locator)
        )
        new_private_tab_element.click()
        print("Clicked on 'New Private Tab' option")

        # Step 2: Verify incognito container is visible
        incognito_container_locator = (
            AppiumBy.ID,
            "com.santa.web3.browser:id/new_tab_incognito_container"
        )
        incognito_container = wait.until(
            EC.visibility_of_element_located(incognito_container_locator)
        )

        if incognito_container.is_displayed():
            print("PASS: New private tab opened successfully.")
        else:
            print("FAIL: Incognito container found but not visible.")

    except Exception as e:
        print(f"FAIL: New private tab did not open. Error: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    test_open_new_private_tab()