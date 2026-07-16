import re
import time

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException
)

print("\n========== TEST STARTED ==========\n")

# =====================================================
# Desired Capabilities
# =====================================================

PACKAGE_NAME = "com.santa.web3.browser"
APP_ACTIVITY = "com.google.android.apps.chrome.Main"
APPIUM_SERVER = "http://127.0.0.1:4723"

options = UiAutomator2Options()
options.platform_name = "Android"
options.device_name = "Android Device"
options.automation_name = "UiAutomator2"

options.app_package = PACKAGE_NAME
options.app_activity = APP_ACTIVITY

# Don't clear app data
options.no_reset = True

driver = webdriver.Remote(
    APPIUM_SERVER,
    options=options
)

wait = WebDriverWait(driver, 30)

TEST_PASSED = False

# =====================================================
# Coin watchlist settings
# =====================================================

# Exact text captured from the device (price/percent change constantly,
# so this is tried first, then we fall back to matching by coin symbol).
COIN_ITEM_EXACT_TEXT = "coin-icon $64323 Btc -1%"
COIN_ITEM_SYMBOL = "Btc"

COIN_ITEM_EXACT_XPATH = (
    '//android.widget.Button[@text="' + COIN_ITEM_EXACT_TEXT + '"]'
)
COIN_ITEM_CONTAINS_XPATH = (
    '//android.widget.Button[contains(@text, "coin-icon") and contains(@text, "'
    + COIN_ITEM_SYMBOL + '")]'
)

URL_BAR_ID = "com.santa.web3.browser:id/url_bar"

def scroll_up_half_screen():
    size = driver.get_window_size()
    width = size["width"]
    height = size["height"]

    start_x = width // 2
    start_y = int(height * 0.75)
    end_y = start_y - 200

    driver.swipe(start_x, start_y, start_x, end_y, 700)

    print(f"Step 2: Scrolled up by {height // 2}px (half of screen height).")


def locate_coin_item():
    try:
        element = driver.find_element(AppiumBy.XPATH, COIN_ITEM_EXACT_XPATH)
        return element, "exact"
    except NoSuchElementException:
        pass

    try:
        element = driver.find_element(AppiumBy.XPATH, COIN_ITEM_CONTAINS_XPATH)
        return element, "symbol"
    except NoSuchElementException:
        return None, None


def extract_coin_symbol(item_text):
    match = re.search(r"coin-icon\s+\$[\d.,]+\s+(\w+)\s*[+-]?\d+(\.\d+)?%", item_text)
    if match:
        return match.group(1)
    return COIN_ITEM_SYMBOL


try:

    # =====================================================
    # Step 1 : Launch / Verify Santa Browser is open
    # =====================================================

    time.sleep(15)

    print("Current Package:", driver.current_package)

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

    assert driver.current_package == PACKAGE_NAME, (
        f"Expected package '{PACKAGE_NAME}' "
        f"but found '{driver.current_package}'"
    )

    print("Step 1: Santa Browser launched successfully.")

    # =====================================================
    # Step 2 : Find and Click Coin Watchlist Item
    # =====================================================

    coin_item, match_type = locate_coin_item()

    if coin_item is None:
        raise NoSuchElementException("Coin watchlist item not found.")

    print(f"Step 2: Coin item found using {match_type} match.")

    scroll_up_half_screen()
    time.sleep(1)

    coin_item, match_type = locate_coin_item()

    if coin_item is None:
        raise NoSuchElementException(
            "Coin watchlist item not found after scrolling."
        )

    assert coin_item.is_displayed(), "Coin watchlist item is not visible after scrolling."

    coin_item_text = coin_item.get_attribute("text") or COIN_ITEM_EXACT_TEXT
    coin_symbol = extract_coin_symbol(coin_item_text)

    print(f"Step 2: Clicking coin watchlist item -> '{coin_item_text}'")

    coin_item.click()

    time.sleep(10)

    print("Step 2: Waited 10s after clicking coin watchlist item.")

    # =====================================================
    # Step 3 : Verify URL Bar Reflects Clicked Coin
    # =====================================================

    url_bar = wait.until(
        EC.visibility_of_element_located(
            (AppiumBy.ID, URL_BAR_ID)
        )
    )

    current_url = url_bar.text.strip()

    assert current_url != "", "URL bar is empty after clicking coin item."

    print("Step 3: URL bar content ->", current_url)

    url_without_query = current_url.split("?")[0].rstrip("/")
    last_path_segment = url_without_query.split("/")[-1]

    print(f"Step 3: Last path segment -> '{last_path_segment}'")
    print(f"Step 3: Expected coin symbol -> '{coin_symbol}'")

    coin_symbol_chars = set(coin_symbol.lower())
    last_segment_chars = set(last_path_segment.lower())

    assert coin_symbol_chars.issubset(last_segment_chars), (
        f"Not all characters of coin symbol '{coin_symbol}' were found in "
        f"last URL path segment '{last_path_segment}'."
    )

    print("Step 3: URL bar verification passed.")

    TEST_PASSED = True

# =====================================================
# Exception Handling
# =====================================================

except TimeoutException:
    print("\n========== TEST FAILED ==========")
    print("Timeout occurred.")
    print(driver.page_source)

except AssertionError as e:
    print("\n========== TEST FAILED ==========")
    print("Assertion Error:", e)
    print(driver.page_source)

except NoSuchElementException:
    print("\n========== TEST FAILED ==========")
    print("Element not found.")
    print(driver.page_source)

except Exception as e:
    print("\n========== TEST FAILED ==========")
    print(e)
    print(driver.page_source)

# =====================================================
# Close Driver
# =====================================================

finally:

    if TEST_PASSED:
        print("\n========== TEST PASSED ==========\n")
    else:
        print("\n========== TEST FAILED ==========\n")

    driver.quit()
