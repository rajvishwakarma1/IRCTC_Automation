import undetected_chromedriver as uc
from time import sleep
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# --- Configure Chrome Options ---
options = uc.ChromeOptions()

# Core evasive arguments (kept for good measure, uc will prioritize if it has its own handling)
options.add_argument("--disable-blink-features=AutomationControlled") # Hides navigator.webdriver (uc does this too)
options.add_argument("--disable-infobars") # Disables "Chrome is being controlled by automated test software" bar
options.add_argument("--disable-extensions") # Disables browser extensions
options.add_argument("--no-sandbox") # Essential for many environments
options.add_argument("--start-maximized") # Ensures it starts maximized
options.add_argument("--incognito") # Ensures a clean session state
options.add_argument("--disable-dev-shm-usage") # Overcomes limited resource problems (Linux, Docker)
options.add_argument("--disable-browser-side-navigation") # Helps with certain navigation issues
options.add_argument("--disable-gpu") # Can sometimes help with WebGL fingerprinting (may impact rendering)
options.add_argument("--no-first-run") # Suppresses initial browser setup
options.add_argument("--no-default-browser-check") # Suppresses "Make default browser" popups
options.add_argument("--lang=en-US") # Set a specific language for consistency
options.add_argument("--disable-background-networking") # Disables background network calls

# Define a realistic User-Agent string
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
options.add_argument(f"user-agent={user_agent}")

# Experimental options (WebDriver preferences)
options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 2, # Block notifications
    "credentials_enable_service": False, # Disable password saving prompt
    "profile.password_manager_enabled": False, # Disable password saving prompt
    "autofill.profile_enabled": False # Disable autofill pop-ups
})


# --- Revised JavaScript Injections (Removed conflicting 'chrome' and 'webdriver' spoofs) ---
stealth_js = """
    // Spoof navigator.plugins, languages, mimetypes (less likely to conflict)
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

    // Overwrite console.debug to prevent logging automation markers
    // This is generally safe and helps clean up console output
    console.debug = () => {};

    // Override MediaDevices.prototype.getUserMedia (to hide microphone/camera access attempts)
    Object.defineProperty(MediaDevices.prototype, 'getUserMedia', {
      get: () => async (constraints) => {
        throw new Error('NotAllowedError: Permission denied');
      }
    });

    // Spoof battery status API
    Object.defineProperty(navigator, 'getBattery', {
      get: () => async () => ({ charging: true, chargingTime: 0, dischargingTime: Infinity, level: 1 })
    });

    // Spoof Permission.query method
    const originalQuery = window.navigator.permissions.query;
    window.navigator.permissions.query = (parameters) =>
        (parameters.name === 'notifications' || parameters.name === 'geolocation') ?
        Promise.resolve({ state: Notification.permission === 'granted' ? 'granted' : 'denied' }) :
        originalQuery(parameters);

    // Randomize getBoundingClientRect (subtle behavioral spoofing)
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

    // Introduce randomized delays to click events
    const originalClick = Element.prototype.click;
    Element.prototype.click = function() {
        const delay = Math.random() * 100 + 50; // 50-150ms delay
        setTimeout(() => originalClick.call(this), delay);
    };

    // Console marker for confirmation that this JS is running
    console.log('undetected chromedriver 1337!');
"""

# --- Initialize the Chrome WebDriver ---
print("Initializing undetected_chromedriver with revised evasive options (minimal JS conflicts)...")
try:
    driver = uc.Chrome(options=options)
    print("undetected_chromedriver initialized successfully.")
except Exception as e:
    print(f"Error initializing undetected_chromedriver: {e}")
    print("Please ensure you have Chrome browser installed and the library is up-to-date.")
    exit()

# Inject the stealth JavaScript
print("Injecting minimalist stealth JavaScript...")
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": stealth_js})


# Open the IRCTC website
print("Navigating to IRCTC website...")
driver.get('https://www.irctc.co.in/nget/train-search')

# Give some initial time for the page to fully load
sleep(random.uniform(5, 10))

# --- Attempt to dismiss notification pop-up if it appears ---
print("Checking for and attempting to dismiss notification pop-up...")
try:
    block_notifications_button = WebDriverWait(driver, 7).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Block') or contains(@aria-label, 'Block') or contains(@class, 'mat-button') and contains(., 'No Thanks')]"))
    )
    driver.execute_script("arguments[0].click();", block_notifications_button)
    print("Notification pop-up 'Block' button clicked.")
    sleep(random.uniform(1, 2))
except Exception as e:
    print(f"Notification pop-up 'Block' button not found or already dismissed: {e}")
    pass

# --- Step 1: Click Login button on main page ---
print("Attempting to click the 'LOGIN' button...")
try:
    login_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@class='search_btn loginText ng-star-inserted']"))
    )
    driver.execute_script("arguments[0].click();", login_button)
    print("Main 'LOGIN' button clicked using JavaScript.")
    sleep(random.uniform(6, 9))
except Exception as e:
    print(f"Error clicking main 'LOGIN' button: {e}")
    print("This might be due to page loading issues or a change in the button's XPath.")
    driver.quit()
    exit()


# --- Step 2: Enter Login Credentials in Pop-up ---
print("Attempting to enter login credentials into the pop-up...")
try:
    username_field = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/app-root/app-home/div[3]/app-login/p-dialog[1]/div/div/div[2]/div[2]/div/div[2]/div/div[2]/form/div[2]/input'))
    )
    # Simulate human typing with random delays
    for char in 'rajvishwakarma303': # <<< IMPORTANT: Replace 'your_username_here'
        username_field.send_keys(char)
        sleep(random.uniform(0.05, 0.2))
    print("Username entered.")
    sleep(random.uniform(0.5, 1.5))

    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/app-root/app-home/div[3]/app-login/p-dialog[1]/div/div/div[2]/div[2]/div/div[2]/div/div[2]/form/div[3]/input'))
    )
    # Simulate human typing with random delays
    for char in 'Raj@321#': # <<< IMPORTANT: Replace 'your_password_here'
        password_field.send_keys(char)
        sleep(random.uniform(0.05, 0.2))
    print("Password entered.")
    sleep(random.uniform(0.5, 1.5))

    captcha_input_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/app-root/app-home/div[3]/app-login/p-dialog[1]/div/div/div[2]/div[2]/div/div[2]/div/div[2]/form/div[5]/div/app-captcha/div/div/input'))
    )
    print("\n--- Automation complete. Username and Password entered. ---")
    print("Due to IRCTC's security, you will STILL need to manually solve ALL CAPTCHAs.")
    print("Please manually enter the CAPTCHA and click 'Sign In' in the browser window.")
    print("If new CAPTCHAs appear after that, please solve them manually as well.")
    print("The browser will remain open for your manual interaction.")
    sleep(3600) # Keep the browser open for a very long time (1 hour) for manual input

except Exception as e:
    print(f"Error finding login fields or CAPTCHA field: {e}")
    print("This might be due to page loading issues or changes in element XPaths.")
    driver.quit()
    exit()