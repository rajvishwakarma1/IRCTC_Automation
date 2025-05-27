from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configuration
USERNAME = "Enter Your Username"
PASSWORD = "Enter your Password"
IRCTC_URL = "https://www.irctc.co.in/nget/train-search"

options = Options()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)

try:
    print("Launching IRCTC site...")
    driver.get(IRCTC_URL)
    driver.maximize_window()

    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    print("Page loaded:", driver.title)

    # Close popup if exists
    try:
        close_popup = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div#disha-banner-close"))
        )
        close_popup.click()
        print("Closed popup.")
    except:
        print("No popup appeared.")

    login_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'LOGIN')]"))
    )
    login_btn.click()
    print("Clicked LOGIN button.")

    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='User Name']"))
    )
    password_input = driver.find_element(By.XPATH, "//input[@placeholder='Password']")

    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    print("Filled username and password.")

    print("Please solve the captcha manually and click SIGN IN.")
    input("Press Enter after logging in manually...")

finally:
    print("Press Enter to close browser...")
    input()
    driver.quit()
