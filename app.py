import undetected_chromedriver as uc
from time import sleep
import random
import json
import datetime
import socket
import signal
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Logging setup
def log_event(event_type, message, extra_data=None):
    log_entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "event_type": event_type,
        "message": message,
        "ip_address": socket.gethostbyname(socket.gethostname())
    }
    if extra_data:
        log_entry.update(extra_data)
    with open("session_logs.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

def handle_exit(signum, frame):
    log_event("exit", "Script terminated manually or browser closed by user.")
    print("\n--- Session Terminated by User or System Signal ---")
    print("------------------------")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

print("------------------------")

options = uc.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--no-sandbox")
options.add_argument("--start-maximized")
options.add_argument("--incognito")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-browser-side-navigation")
options.add_argument("--disable-gpu")
options.add_argument("--no-first-run")
options.add_argument("--no-default-browser-check")
options.add_argument("--lang=en-US")
options.add_argument("--disable-background-networking")

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
options.add_argument(f"user-agent={user_agent}")

options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 2,
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False,
    "autofill.profile_enabled": False
})

stealth_js = """
    Object.defineProperty(navigator, 'plugins', {
      get: () => [
        {name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer'},
        {name: 'Chrome PDF Viewer', filename: 'internal-pdf-viewer'},
        {name: 'Native Client', filename: 'internal-nacl-plugin'}
      ]
    });
    Object.defineProperty(navigator, 'languages', {
      get: () => ['en-US', 'en']
    });
    Object.defineProperty(navigator, 'mimeTypes', {
      get: () => [
        {type: 'application/pdf', suffixes: 'pdf'},
        {type: 'application/x-google-chrome-pdf', suffixes: 'pdf'},
        {type: 'application/x-nacl', suffixes: 'nacl'}
      ]
    });

    console.debug = () => {};

    Object.defineProperty(MediaDevices.prototype, 'getUserMedia', {
      get: () => async (constraints) => {
        throw new Error('NotAllowedError: Permission denied');
      }
    });

    Object.defineProperty(navigator, 'getBattery', {
      get: () => async () => ({ charging: true, chargingTime: 0, dischargingTime: Infinity, level: 1 })
    });

    const originalQuery = window.navigator.permissions.query;
    window.navigator.permissions.query = (parameters) =>
        (parameters.name === 'notifications' || parameters.name === 'geolocation') ?
        Promise.resolve({ state: Notification.permission === 'granted' ? 'granted' : 'denied' }) :
        originalQuery(parameters);

    const originalGetBoundingClientRect = Element.prototype.getBoundingClientRect;
    Element.prototype.getBoundingClientRect = function() {
        const rect = originalGetBoundingClientRect.call(this);
        return {
            x: rect.x + Math.random() * 0.01 - 0.005,
            y: rect.y + Math.random() * 0.01 - 0.005,
            width: rect.width,
            height: rect.height,
            top: rect.top + Math.random() * 0.01 - 0.005,
            right: rect.right + Math.random() * 0.01 - 0.005,
            bottom: rect.bottom + Math.random() * 0.01 - 0.005,
            left: rect.left + Math.random() * 0.01 - 0.005,
        };
    };

    const originalClick = Element.prototype.click;
    Element.prototype.click = function() {
        const delay = Math.random() * 100 + 50;
        setTimeout(() => originalClick.call(this), delay);
    };

    console.log('undetected chromedriver 1337!');
"""

print("Initializing undetected_chromedriver...")
try:
    driver = uc.Chrome(options=options)
    log_event("driver_init", "ChromeDriver initialized successfully.")
except Exception as e:
    log_event("driver_error", f"Error initializing ChromeDriver: {e}")
    exit()

print("Injecting stealth JavaScript...")
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": stealth_js})

print("Navigating to IRCTC website...")
driver.get('https://www.irctc.co.in/nget/train-search')
log_event("navigate", "Navigated to IRCTC website.")

sleep(random.uniform(5, 10))

print("Checking for notification pop-up...")
try:
    block_btn = WebDriverWait(driver, 7).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Block') or contains(@aria-label, 'Block') or contains(@class, 'mat-button') and contains(., 'No Thanks')]"))
    )
    driver.execute_script("arguments[0].click();", block_btn)
    log_event("notification_dismissed", "Notification pop-up dismissed.")
except Exception as e:
    log_event("notification_skip", f"No notification pop-up found or already dismissed: {e}")

print("Attempting to click LOGIN button...")
try:
    login_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@class='search_btn loginText ng-star-inserted']"))
    )
    driver.execute_script("arguments[0].click();", login_button)
    log_event("login_click", "Login button clicked.")
    sleep(random.uniform(6, 9))
except Exception as e:
    log_event("login_click_fail", f"Login button click failed: {e}")
    driver.quit()
    exit()

print("Filling in login form...")
try:
    username_field = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/app-root/app-home/div[3]/app-login/p-dialog[1]/div/div/div[2]/div[2]/div/div[2]/div/div[2]/form/div[2]/input'))
    )
    for char in 'Enter Username Here':
        username_field.send_keys(char)
        sleep(random.uniform(0.05, 0.2))
    log_event("username_entered", "Username filled.")

    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/app-root/app-home/div[3]/app-login/p-dialog[1]/div/div/div[2]/div[2]/div/div[2]/div/div[2]/form/div[3]/input'))
    )
    for char in 'Enter Password Here':
        password_field.send_keys(char)
        sleep(random.uniform(0.05, 0.2))
    log_event("password_entered", "Password filled.")

    captcha_input_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/app-root/app-home/div[3]/app-login/p-dialog[1]/div/div/div[2]/div[2]/div/div[2]/div/div[2]/form/div[5]/div/app-captcha/div/div/input'))
    )
    log_event("captcha_displayed", "CAPTCHA field detected. Awaiting manual fill.")

    print("\n--- Automation complete. Username and Password entered. ---")
    print("Please manually enter the CAPTCHA and click 'Sign In' in the browser window.")

    while True:
        input("\nAfter filling each CAPTCHA and clicking Sign In, press Enter here to log the event.")
        log_event("captcha_filled", "CAPTCHA submitted manually by user.")
except Exception as e:
    log_event("form_fill_error", f"Login form fill failed: {e}")
    driver.quit()
    exit()
