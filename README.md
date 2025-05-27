# IRCTC Login Automation Tool

This repository contains a Python-based automation tool designed to navigate the IRCTC login process using Selenium, incorporating CAPTCHA solving and robust session management.

## 🛠 Tools Used

* **Python 3.7+**

* **Selenium WebDriver**

* **Google Chrome + ChromeDriver**

## 📺 Demo

You can watch a demo of the automation tool in action here: <https://youtu.be/rV3QRSc5YCw>

## 🧠 My Approach

The automation simulates a user login on the IRCTC website, ensuring session persistence and usability while strictly adhering to ethical usage practices.

### Browser Launch & Setup

* The script leverages Selenium to launch Google Chrome with a maximized window.

* Extensions are disabled to optimize performance and reduce potential interference.

* A standard user agent is employed to minimize the risk of detection.

### Navigate to Login Page

* The browser automatically directs to the IRCTC homepage.

* The script intelligently waits for the "Login" button to become clickable before initiating the click action.

### Login & CAPTCHA Handling

* IRCTC utilizes a complex CAPTCHA mechanism that cannot be programmatically solved by automation tools due to its inherent complexity and legal considerations.

* The user is prompted to manually input their username, password in the terminal, and complete the CAPTCHA.

* Upon successful completion, the user presses `Enter` in the terminal, allowing the script to resume its automated flow.

### Navigating to Book Ticket Page

* Following a successful login, the automation seamlessly navigates directly to the "Book Ticket" page, simulating a realistic user journey.

### Session Management

* IRCTC sessions are known for their quick timeouts due to inactivity.

* To counteract this, the script simulates periodic browser activity (e.g., page reloads or minor DOM interactions) at intervals of 30–60 seconds. This proactive measure aims to keep the session alive for a minimum of 2 minutes.

### Error Handling & Logging

* In the event of any operational error (such as an element not being found or a timeout), a screenshot is automatically captured and saved in the `screenshots/` directory for effective troubleshooting.

* Comprehensive logs are maintained throughout the process to aid in debugging and verifying the automation's behavior.

### Graceful Cleanup

* Once the session concludes or the script completes its designated tasks, the browser is automatically closed, and all associated resources are meticulously cleaned up.

## ⏱ Time Spent

Approximately 6 hours were dedicated to the development and refinement of this tool.

## 💡 Notes

* **CAPTCHA solving is a mandatory step** — the script will pause, awaiting user input.

* Chrome operates in a **visible (non-headless) mode** to facilitate easier interaction and demonstration.

* The tool is meticulously designed to **avoid detection** and strictly **comply with IRCTC's fair usage policies**.

* **No user credentials or sensitive data are stored** by the script.

## 📜 Run Instructions

To execute this automation tool, follow these steps:

```bash
# Clone the repository
git clone <repository-url>
cd irctc-automation

# Install dependencies
pip install -r requirements.txt

# Run the automation
python main.py
