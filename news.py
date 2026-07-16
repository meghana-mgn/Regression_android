import time

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException
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

options.no_reset = True

driver = webdriver.Remote(
    APPIUM_SERVER,
    options=options
)

wait = WebDriverWait(driver, 30)

TEST_PASSED = False

# =====================================================
# Scroll settings
# =====================================================

MAX_SCROLLS = 8
SEARCH_BOX_ID = "com.santa.web3.browser:id/search_box"
LOCATION_BAR_ID = "com.santa.web3.browser:id/location_bar"
URL_BAR_ID = "com.santa.web3.browser:id/url_bar"
NTP_OVERLAY_ID = "com.santa.web3.browser:id/ntp_overlay"
OPTIONAL_TOOLBAR_BUTTON_XPATH = '//*[contains(@resource-id, ":id/optional_toolbar_button")]'
SEARCH_BOX_TOP_TARGET = 300
NUMBER_OF_ARTICLES_TO_CLICK = 3
MAX_EXTRA_SCROLLS_PER_ARTICLE = 15

# Track clicked articles by (title, rounded_y) to reduce false-dedup
# in case two different articles share the same title text
clicked_article_keys = set()


def swipe_up(driver):
    size = driver.get_window_size()
    width = size["width"]
    height = size["height"]

    driver.swipe(
        width // 2,
        int(height * 0.82),
        width // 2,
        int(height * 0.22),
        700
    )


def small_swipe_up(driver):
    size = driver.get_window_size()
    width = size["width"]
    height = size["height"]

    driver.swipe(
        width // 2,
        int(height * 0.68),
        width // 2,
        int(height * 0.48),
        500
    )


def get_search_bar_position():
    for element_name, element_id in (
        ("NTP search box", SEARCH_BOX_ID),
        ("Top location bar", LOCATION_BAR_ID),
        ("Top URL bar", URL_BAR_ID),
    ):
        try:
            element = driver.find_element(AppiumBy.ID, element_id)

            if element.is_displayed():
                return element_name, element.location["y"]

        except NoSuchElementException:
            continue

    raise NoSuchElementException("Search bar was not found.")


def wait_for_ntp():
    ntp_element = wait.until(
        EC.visibility_of_element_located((AppiumBy.ID, NTP_OVERLAY_ID))
    )
    assert ntp_element.is_displayed(), "NTP is not displayed."
    return ntp_element


def scroll_until_search_bar_reaches_top():
    for i in range(MAX_SCROLLS):
        search_bar_name, search_bar_top = get_search_bar_position()
        print(f"Scroll: {search_bar_name} top is {search_bar_top}.")

        if search_bar_top <= SEARCH_BOX_TOP_TARGET:
            print("Scroll: Search bar reached the top area.")
            break

        swipe_up(driver)
        print(f"Scroll: Swipe #{i + 1} performed.")
        time.sleep(1)
    else:
        raise AssertionError("Search bar did not reach the top after scrolling.")


def get_visible_news_articles():
    screen_height = driver.get_window_size()["height"]
    clickable_views = driver.find_elements(
        AppiumBy.XPATH,
        '//android.webkit.WebView//android.view.View[@clickable="true"]'
    )

    articles = []

    for view in clickable_views:
        try:
            if not view.is_displayed():
                continue

            location = view.location
            size = view.size

            if size["width"] < 600 or size["height"] < 250:
                continue

            if location["y"] < 450 or location["y"] >= screen_height:
                continue

            images = view.find_elements(AppiumBy.CLASS_NAME, "android.widget.Image")
            text_views = view.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
            title = ""

            for text_view in text_views:
                text = text_view.text.strip()
                if text:
                    title = text
                    break

            if images and title:
                articles.append((location["y"], title, view))

        except (NoSuchElementException, StaleElementReferenceException):
            continue

    articles.sort(key=lambda item: item[0])
    return articles


def make_article_key(y_position, title):
    # Round y to reduce sensitivity to tiny pixel shifts between scrolls
    return (title, round(y_position / 50) * 50)


def find_next_unclicked_article():
    """
    Looks at currently visible articles first (no scroll-to-top).
    If all visible ones are already clicked, scrolls down further
    from the CURRENT position until a new one appears.
    Uses bigger swipes if small ones aren't revealing new content.
    """
    last_articles_seen = None
    stagnant_count = 0

    for i in range(MAX_EXTRA_SCROLLS_PER_ARTICLE):
        articles = get_visible_news_articles()

        # ---- DEBUG: show what we currently see ----
        print(f"Debug: Attempt #{i + 1} -> {len(articles)} article(s) visible:")
        for y, title, _ in articles:
            key = make_article_key(y, title)
            marker = "(ALREADY CLICKED)" if key in clicked_article_keys else "(NEW)"
            print(f"    y={y}, title='{title}' {marker}")

        for y, title, view in articles:
            key = make_article_key(y, title)
            if key not in clicked_article_keys:
                print(f"Scroll: Found new unclicked article -> {title} "
                      f"(after {i} extra scroll(s) from current position).")
                return title, key, view

        # Detect if scrolling is stuck (same articles seen repeatedly)
        current_titles = tuple(a[1] for a in articles)
        if current_titles == last_articles_seen:
            stagnant_count += 1
        else:
            stagnant_count = 0
        last_articles_seen = current_titles

        # If stuck for 3 checks in a row, try a BIGGER swipe instead
        if stagnant_count >= 3:
            print("Scroll: Content not changing with small swipes, "
                  "trying a bigger swipe.")
            swipe_up(driver)
        else:
            small_swipe_up(driver)

        print(f"Scroll: Extra scroll #{i + 1} performed "
              f"(all visible articles already clicked).")
        time.sleep(2)

    raise AssertionError(
        "Could not find a new, unclicked news article after scrolling. "
        "This may mean the news feed has no more unique articles loaded, "
        "or the page has reached its scroll limit."
    )


def click_plus_button_to_open_ntp():
    plus_button = wait.until(
        EC.element_to_be_clickable((AppiumBy.XPATH, OPTIONAL_TOOLBAR_BUTTON_XPATH))
    )

    assert plus_button.is_displayed(), "Plus button is not visible after redirection."
    plus_button.click()
    print("Click: '+' button clicked to open NTP.", flush=True)

    wait_for_ntp()
    time.sleep(1)
    print("Verify: NTP opened successfully.", flush=True)


try:

    # =====================================================
    # Step 1 : Verify NTP is Visible
    # =====================================================

    wait_for_ntp()

    print("Step 1: NTP is displayed successfully.")

    # =====================================================
    # Step 2 : Scroll to News Section ONCE, Before the Loop
    # =====================================================

    scroll_until_search_bar_reaches_top()

    # =====================================================
    # Step 3 : For Each Article -> Find Next New One, Click, Verify
    # =====================================================

    for article_number in range(1, NUMBER_OF_ARTICLES_TO_CLICK + 1):

        print(f"\n--- Processing news article #{article_number} ---")

        title, key, article = find_next_unclicked_article()

        print(f"Click: Clicking news article -> {title}", flush=True)
        article.click()

        clicked_article_keys.add(key)

        time.sleep(5)  # buffer for redirect / page load

        click_plus_button_to_open_ntp()

        print(f"Result: Article #{article_number} processed successfully "
              f"-> {title}")

    print("\nAll news articles processed successfully.")

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