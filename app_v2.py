from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

USERNAME = "YOUR_IRCTC_USERNAME"
PASSWORD = "YOUR_IRCTC_PASSWORD"
IRCTC_URL = "https://www.irctc.co.in/nget/train-search"
SESSION_ALIVE_DURATION_MINS = 2

options = Options()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

print("Initializing Chrome WebDriver...")
driver = webdriver.Chrome(options=options)

try:
    print(f"Navigating to IRCTC website: {IRCTC_URL}")
    driver.get(IRCTC_URL)
    driver.maximize_window()

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    print(f"Page loaded successfully. Title: '{driver.title}'")

    try:
        print("Checking for and attempting to close the Disha chatbot popup...")
        close_popup_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div#disha-banner-close"))
        )
        close_popup_button.click()
        print("Disha chatbot popup closed.")
    except TimeoutException:
        print("Disha chatbot popup not found within the timeout period.")
    except Exception as e:
        print(f"An issue occurred while trying to close the popup: {e}")

    print("Locating and clicking the 'LOGIN' button...")
    login_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'LOGIN')]"))
    )
    login_button.click()
    print("Clicked 'LOGIN' button. Waiting for login form...")

    print("Locating username and password fields...")
    username_field = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='User Name']"))
    )
    password_field = driver.find_element(By.XPATH, "//input[@placeholder='Password']")

    username_field.send_keys(USERNAME)
    password_field.send_keys(PASSWORD)
    print("Username and password filled.")

    print("\n--- IMPORTANT: MANUAL INTERVENTION REQUIRED ---")
    print("Please solve the CAPTCHA in the browser window that just opened.")
    print("After solving the captcha, press 'Enter' in this console to continue the script.")
    input("Press Enter AFTER you have filled the CAPTCHA and BEFORE clicking 'SIGN IN'...")
    print("User confirmed captcha entry. Attempting to click 'SIGN IN'...")

    try:
        sign_in_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='SIGN IN']"))
        )
        sign_in_button.click()
        print("Clicked 'SIGN IN' button.")
    except TimeoutException:
        print("SIGN IN button not found or not clickable within the timeout. This might indicate the login form didn't load correctly or an immediate issue occurred.")
        input("Press Enter to manually inspect the browser before closing...")
        raise
    except Exception as e:
        print(f"An issue occurred while trying to click 'SIGN IN': {e}")
        input("Press Enter to manually inspect the browser before closing...")
        raise

    print("Loading...")
    print("Successfully loaded.")

    print(f"Keeping session alive for {SESSION_ALIVE_DURATION_MINS} minutes by simulating interaction and monitoring session status...")
    end_time = time.time() + (SESSION_ALIVE_DURATION_MINS * 60)
    interaction_interval = 20

    while time.time() < end_time:
        driver.execute_script("window.scrollBy(0, 200);")
        driver.execute_script("window.scrollBy(0, -100);")
        remaining_time = int(end_time - time.time())
        print(f"Session refreshed. Reminder: Script is working. Time remaining: {remaining_time} seconds.")

        current_url = driver.current_url
        if "session-expired" in current_url or "login" in current_url.lower() and "train-search" not in current_url.lower():
            print("Session appears to have concluded based on URL change. Exiting session keep-alive.")
            break

        if time.time() + interaction_interval > end_time:
            time.sleep(max(0, end_time - time.time()))
        else:
            time.sleep(interaction_interval)

    print(f"Session activity concluded after {SESSION_ALIVE_DURATION_MINS} minutes or session conclusion. Automation complete.")

except Exception as e:
    print(f"\nAn unexpected issue occurred during the automation: {e}")
    print("Please inspect the browser window for details.")

finally:
    print("\nAutomation finished. Closing browser automatically.")
    driver.quit()
    print("Browser closed.")
