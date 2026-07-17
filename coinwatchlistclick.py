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

COIN_ITEMS_XPATH = '//android.widget.Button[contains(@text, "coin-icon")]'
OPTIONAL_TOOLBAR_BUTTON_XPATH = '//*[contains(@resource-id, ":id/optional_toolbar_button")]'
NTP_OVERLAY_ID = "com.santa.web3.browser:id/ntp_overlay"
URL_BAR_ID = "com.santa.web3.browser:id/url_bar"

# Maps the coin symbol shown in the watchlist (e.g. "Btc") to the coin name
# used in the redirected page's URL (e.g. "bitcoin").
COIN_SYMBOL_TO_NAME = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "usdt": "tether",
    "bnb": "bnb",
    "usdc": "usd-coin",
    "xrp": "ripple",
    "ada": "cardano",
    "doge": "dogecoin",
    "sol": "solana",
    "trx": "tron",
    "dot": "polkadot",
    "matic": "polygon",
    "ltc": "litecoin",
    "shib": "shiba-inu",
    "avax": "avalanche-2",
}


def scroll_up_half_screen():
    size = driver.get_window_size()
    width = size["width"]
    height = size["height"]

    start_x = width // 2
    start_y = int(height * 0.75)
    end_y = start_y - 200

    driver.swipe(start_x, start_y, start_x, end_y, 700)

    print(f"Step 2: Scrolled up by {height // 2}px (half of screen height).")


def get_coin_item_count():
    items = driver.find_elements(AppiumBy.XPATH, COIN_ITEMS_XPATH)
    return len(items)


def get_coin_item_by_position(position):
    xpath = f'({COIN_ITEMS_XPATH})[{position}]'
    return driver.find_element(AppiumBy.XPATH, xpath)


def wait_for_coin_watchlist(max_attempts=6):
    for attempt in range(max_attempts):
        count = get_coin_item_count()

        if count > 0:
            first_item = get_coin_item_by_position(1)
            if first_item.is_displayed():
                print(f"Step 2: Coin watchlist visible with {count} item(s) "
                      f"(after {attempt} extra scroll(s)).")
                return count

        print(f"Step 2: Coin watchlist not visible yet, scrolling "
              f"(attempt {attempt + 1}/{max_attempts}).")
        scroll_up_half_screen()
        time.sleep(6)

    raise NoSuchElementException(
        "Coin watchlist items not found after scrolling."
    )


def extract_coin_symbol(item_text):
    match = re.search(r"coin-icon\s+\$[\d.,]+\s+(\w+)\s*[+-]?\d+(\.\d+)?%", item_text)
    if not match:
        raise AssertionError(f"Could not extract coin symbol from '{item_text}'.")
    return match.group(1)


def get_expected_coin_name(coin_symbol):
    coin_name = COIN_SYMBOL_TO_NAME.get(coin_symbol.lower())
    if coin_name is None:
        raise AssertionError(
            f"No known coin name mapping for symbol '{coin_symbol}'. "
            f"Add it to COIN_SYMBOL_TO_NAME."
        )
    return coin_name


def scroll_left_for_coin_item(position, item_width, container_y):
    scroll_distance = (position - 1) * item_width

    if scroll_distance <= 0:
        print(f"Step 2: [{position}] No horizontal scroll needed.")
        return

    size = driver.get_window_size()
    width = size["width"]

    # start_x = width - 60 # start x seem not correct, we need start_x = center of horizontal screen
    size = driver.get_window_size()
    width = size["width"]

    start_x = width // 2
  
    end_x = start_x - scroll_distance

    driver.swipe(start_x, container_y, end_x, container_y, 800)
    time.sleep(1)

    print(f"Step 2: [{position}] Scrolled coin watchlist left by "
          f"{scroll_distance}px ((position - 1) * item width).")


def click_plus_button_to_open_ntp():
    plus_button = wait.until(
        EC.element_to_be_clickable((AppiumBy.XPATH, OPTIONAL_TOOLBAR_BUTTON_XPATH))
    )

    assert plus_button.is_displayed(), "'+' button is not visible."

    plus_button.click()

    print("Navigation: '+' button clicked to return to NTP.")

    ntp_element = wait.until(
        EC.visibility_of_element_located((AppiumBy.ID, NTP_OVERLAY_ID))
    )
    assert ntp_element.is_displayed(), "NTP is not displayed after returning."

    time.sleep(2)


def verify_coin_item(position, item_width, container_y):
    scroll_left_for_coin_item(position, item_width, container_y)

    coin_item = get_coin_item_by_position(position)
    assert coin_item.is_displayed(), f"Coin item #{position} is not visible."

    coin_item_text = coin_item.get_attribute("text") or ""
    coin_symbol = extract_coin_symbol(coin_item_text)

    print(f"Step 2: [{position}] Clicking coin watchlist item -> '{coin_item_text}'")

    coin_item.click()

    time.sleep(10)

    print(f"Step 2: [{position}] Waited 10s after clicking coin watchlist item.")

    # =====================================================
    # Step 3 : Verify URL Bar Reflects Clicked Coin
    # =====================================================

    url_bar = wait.until(
        EC.visibility_of_element_located((AppiumBy.ID, URL_BAR_ID))
    )

    current_url = url_bar.text.strip()

    assert current_url != "", f"URL bar is empty after clicking coin item #{position}."

    print(f"Step 3: [{position}] URL bar content -> {current_url}")

    url_without_query = current_url.split("?")[0].rstrip("/")
    last_path_segment = url_without_query.split("/")[-1]

    expected_coin_name = get_expected_coin_name(coin_symbol)

    print(f"Step 3: [{position}] Last path segment -> '{last_path_segment}', "
          f"coin symbol -> '{coin_symbol}', expected coin name -> '{expected_coin_name}'")

    assert expected_coin_name.lower() in last_path_segment.lower(), (
        f"[{position}] Expected coin name '{expected_coin_name}' (for symbol "
        f"'{coin_symbol}') not found in last URL path segment '{last_path_segment}'."
    )

    print(f"Step 3: [{position}] URL bar verification passed for "
          f"'{coin_symbol}' -> '{expected_coin_name}'.")


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
    # Step 2 & 3 : Verify Every Coin Watchlist Item
    # =====================================================

    scroll_up_half_screen()
    time.sleep(5)
  
    coin_count = wait_for_coin_watchlist()

    print(f"Step 2: Found {coin_count} coin watchlist item(s).")

    for position in range(1, coin_count + 1):

        print(f"\n--- Verifying coin watchlist item #{position} of {coin_count} ---")

        # Re-measure the row every time: its vertical position can shift
        # between page loads (e.g. ad banners pushing content down).
        first_item = get_coin_item_by_position(1)
        assert first_item.is_displayed(), "First coin watchlist item is not visible."

        item_width = first_item.size["width"]
        container_y = first_item.location["y"] + first_item.size["height"] // 2

        verify_coin_item(position, item_width, container_y)

        if position < coin_count:
            click_plus_button_to_open_ntp()
            wait_for_coin_watchlist()

    print(f"\nAll {coin_count} coin watchlist item(s) verified successfully.")

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
