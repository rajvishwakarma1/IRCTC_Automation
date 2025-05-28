# IRCTC Login Automation Tool

This repository contains a Python-based automation tool designed to assist with the initial steps of the IRCTC login process. Due to sophisticated anti-bot measures and dynamic CAPTCHA challenges implemented by IRCTC, the tool automates the initial form filling, leaving the CAPTCHA resolution and subsequent login steps for manual user interaction.

## 🛠 Tools Used

* **Python 3.7+**

* **Selenium WebDriver**

* **undetected_chromedriver** (for enhanced anti-detection capabilities)

* **Google Chrome + ChromeDriver**

## 📺 Demo

You can watch a demo of the automation tool in action here: <https://youtu.be/TPCkSHVbVgE>

## 🧠 My Approach

The automation aims to simulate a user's initial interaction with the IRCTC login, focusing on reliable form filling while acknowledging the limitations imposed by advanced bot detection.

### Browser Launch & Setup

* The script leverages `undetected_chromedriver` to launch Google Chrome, which is specifically designed to bypass common Selenium detection methods.

* Chrome is launched in **incognito mode** to ensure a clean session without pre-existing cookies or cached data.

* The browser window is automatically maximized, and various Chrome options (e.g., disabling infobars, extensions, background networking) are applied to further minimize detection risks.

* A realistic user agent string is employed, and subtle JavaScript injections are executed on new document loads to spoof browser properties (like `navigator.plugins`, `navigator.languages`, `window.chrome` properties, `getBattery`, `getUserMedia`, and `Permissions.query`) and introduce randomized delays in DOM interactions (like `getBoundingClientRect` and `click` events), making the automated session appear more human-like.

### Navigate to Login Page

* The browser automatically directs to the IRCTC homepage.

* The script intelligently waits for the "Login" button to become clickable before initiating the click action using JavaScript for robustness.

### Login & CAPTCHA Handling (Hybrid Approach)

* IRCTC utilizes a complex and dynamic CAPTCHA mechanism that **cannot be programmatically solved** by automation tools due to its inherent complexity, legal considerations, and active anti-bot measures.

* The script will **automatically input your username and password** into the respective fields in the login modal.

* **After filling the credentials, the script will pause indefinitely (for 1 hour) and keep the browser open.** At this point, the user is prompted to **manually input the CAPTCHA** displayed in the browser window and then **manually click the "SIGN IN" button.**

* **Important:** If IRCTC presents *additional* CAPTCHAs or verification steps after the first "SIGN IN" attempt, these will also need to be solved manually by the user.

### Post-Login Actions (Manual)

* Due to the dynamic nature of IRCTC's anti-bot systems and the requirement for manual CAPTCHA solving, **subsequent navigation to the "Book Ticket" page or any other post-login actions are NOT automated by this script.** The script's primary function concludes once the username and password are filled, and it awaits your manual login completion.

### Session Management (Manual)

* Given the manual intervention required for CAPTCHAs, automated session management (like periodic activity to prevent timeouts) is not implemented. The session's persistence after login will depend on your manual interactions.

### Error Handling & Logging

* In the event of any operational error during the automated steps (such as an element not being found or a timeout), a relevant message is printed to the terminal.

* Comprehensive logs are maintained in the terminal throughout the process to aid in debugging and verifying the automation's behavior.

### Graceful Cleanup

* The script is designed to **keep the browser open** after completing its automated tasks, allowing for manual user interaction and observation of the login process. The browser will not automatically close until you manually close it or the script's long pause (`sleep(3600)`) expires.

## Evasion Techniques

This tool employs several techniques to minimize the chances of being detected by sophisticated anti-bot systems, such as those used by IRCTC:

* **`undetected_chromedriver`:** This is the primary library used. It patches the standard ChromeDriver to hide common automation fingerprints, such as the `navigator.webdriver` property, making the browser appear more like a regular user's browser.

* **Chrome Options Configuration:**

  * **`--disable-blink-features=AutomationControlled`**: Explicitly tells Chrome to disable features that reveal automation.

  * **`--disable-infobars`**: Removes the "Chrome is being controlled by automated test software" bar.

  * **`--disable-extensions`**: Prevents extensions from loading, which can sometimes be a detection point.

  * **`--no-sandbox`**: Disables the sandbox, often used in containerized environments.

  * **`--start-maximized`**: Ensures the browser window starts maximized, providing consistent window dimensions.

  * **`--incognito`**: Launches the browser in incognito mode for a clean session state, free from previous cookies or cache.

  * **`--disable-dev-shm-usage`**: Addresses potential issues with shared memory in Linux environments.

  * **`--disable-browser-side-navigation`**: Can help with certain Single Page Application (SPA) navigation patterns.

  * **`--disable-gpu`**: May alter WebGL fingerprinting, though it can impact rendering performance.

  * **`--no-first-run` & `--no-default-browser-check`**: Suppress initial browser setup and default browser prompts.

  * **`--lang=en-US`**: Sets a consistent browser language.

  * **`--disable-background-networking`**: Disables background network activity that might be atypical for a human user.

  * **Realistic User-Agent**: A common, up-to-date user-agent string is explicitly set to mimic a standard browser.

  * **Experimental Preferences (`prefs`):** Configures Chrome preferences to block notifications, disable password saving prompts, and autofill features.

* **JavaScript Injections (`Page.addScriptToEvaluateOnNewDocument`):** Custom JavaScript is injected into every new document loaded to further spoof browser properties and behaviors:

  * **`navigator.plugins`, `navigator.languages`, `navigator.mimeTypes`**: These properties are spoofed to contain values consistent with a regular browser.

  * **`console.debug`**: Overwritten to prevent logging of potential automation markers.

  * **`MediaDevices.prototype.getUserMedia`**: Overridden to prevent detection from attempts to access microphone/camera.

  * **`navigator.getBattery`**: Spoofed to return a consistent battery status.

  * **`Permissions.query`**: Spoofed to return consistent permission states (e.g., for notifications, geolocation).

  * **Behavioral Spoofing**: Subtle random variations are introduced to `Element.prototype.getBoundingClientRect` (for element position readings) and `Element.prototype.click` (for click event delays) to make interactions less robotic.

## 🗂 Logging & Monitoring

The tool now supports **session logging** in a structured `.jsonl` format (`session_logs.jsonl`) with these key features:

### ✅ Logged Events
* Driver/browser launch and exit
* Navigation to IRCTC
* Login modal interaction
* Username/password input
* Manual CAPTCHA fill events
* Browser closure (user-initiated or via script)
* IP address of the session

### 📌 Log Format
Each entry includes:

```json
{ "timestamp": "2025-05-28T12:34:56", "event": "captcha_filled", "message": "User manually filled captcha", "ip": "123.45.67.89" }
```

### 📎 Additional Features
* IP detection for each session
* Detects if the user closes the browser manually
* Logs every time the CAPTCHA is filled
* Adds `------------------------` line between sessions for clarity

## ❌ Challenges and Limitations (Why Full Automation Was Not Achieved)

Despite employing extensive evasion techniques, full automation of the IRCTC login process proved unfeasible due to the highly sophisticated anti-bot measures implemented by the website. Key challenges encountered include:

* **Persistent CAPTCHA Chaining:** IRCTC's system actively detects automated browser sessions. Upon detecting automation, it frequently presents multiple, dynamic CAPTCHAs in a continuous loop. These CAPTCHAs are designed to be human-solvable and cannot be programmatically bypassed by automation tools. This behavior is a primary defense mechanism to prevent non-human logins.

* **Server-Side Blocking (504 Gateway Timeout):** Even when client-side browser fingerprints were effectively masked using `undetected_chromedriver` and custom JavaScript injections, the IRCTC server would often respond with `504 Gateway Timeout` errors. This indicates that the server-side anti-bot system was identifying and blocking the automated requests at a network or load-balancer level, preventing the requests from even reaching the main application logic. The fact that manual login attempts from the same machine and network were successful confirmed that these 504 errors were a direct response to detected automation, rather than general server downtime.

* **Dynamic Website Behavior:** IRCTC's website frequently updates its structure and security protocols, making it a continuous challenge to maintain consistent automation without constant adaptation of XPaths and evasion strategies.

These combined factors demonstrate that IRCTC is highly effective at preventing automated logins, necessitating manual intervention for the CAPTCHA and final login steps.

## ⏱ Time Spent

Approximately 6+ hours were dedicated to the development and refinement of this tool, primarily focused on addressing anti-bot detection and ensuring reliable initial form filling.

## 💡 Notes

* **CAPTCHA solving is a mandatory manual step** — the script will pause, awaiting user input for *all* CAPTCHAs presented.

* Chrome operates in a **visible (non-headless) mode** to facilitate easier manual interaction and observation.

* The tool is meticulously designed to **avoid detection** and strictly **comply with IRCTC's fair usage policies**. However, IRCTC's anti-bot measures are highly sophisticated and may still result in server errors (e.g., 504 Gateway Timeout) or repeated CAPTCHAs, even with evasive techniques.

* **No user credentials or sensitive data are stored** by the script.

## 📜 Run Instructions

To execute this automation tool, follow these steps:

```bash
# Clone the repository (replace <repository-url> with your actual repo URL)
git clone <repository-url>
cd irctc-automation

# Install dependencies
pip install -r requirements.txt
# Ensure you also have undetected_chromedriver installed:
pip install undetected_chromedriver

# Run the automation
python main.py
```
