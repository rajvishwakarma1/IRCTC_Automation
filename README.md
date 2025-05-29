# IRCTC Login Automation Tool

This repository contains a **Python-based automation tool** designed to assist with the IRCTC login process, including **automated CAPTCHA solving**, structured session logging, and stealth browser emulation. It now integrates with **Patchright Python** for stable rendering and interaction, and uses an OCR-based solution to fill in CAPTCHAs automatically — reducing manual input while staying within IRCTC's human-safety limits.

---

## 🛠 Tools Used

* **Python 3.7+**
* **Patchright Python** (headless Chromium automation)
* **OCR.Space API** (for CAPTCHA solving)
* **Pillow + OpenCV** (for image preprocessing)
* **Structured logging with JSONL + CSV export**

---

## 📺 Demo

[Watch on YouTube](https://youtu.be/e2hcYkBKBAU)

---

## 🚀 New: Patchright + OCR-Based CAPTCHA Automation

### ✅ What's Automated:
- Launches browser using Patchright
- Navigates to IRCTC homepage
- Clicks Login → Enters username/password
- Captures CAPTCHA image
- Preprocesses CAPTCHA and solves using OCR
- Fills CAPTCHA input field
- Clicks "SIGN IN" automatically
- Waits on Book Ticket page (180 seconds)
- Logs session stats in JSONL format

### ⚠️ What Still Needs Human Help:
- If CAPTCHA fails, it will retry up to 8 times
- If loop is detected, it logs and exits gracefully
- Additional security layers (like OTP, puzzles) are not handled

---

## 📦 Folder Structure

```bash
.
├── app.py                 # Main automation script
├── ocr_utils.py          # CAPTCHA preprocessing + OCR logic
├── analyze_logs.py       # Log summary + CSV export
├── session_logs.jsonl    # Structured session logs
├── session_report.csv    # Summary metrics
├── requirements.txt
└── README.md
```

## 📷 CAPTCHA Solving via OCR

CAPTCHA solving uses:

- Grayscale conversion
- Contrast boosting
- Thresholding
- OCR.Space API for recognition
- Regex cleanup to sanitize OCR output

If CAPTCHA is incorrect:

- Logs retry
- Detects CAPTCHA loop
- Exits gracefully after 8 attempts

## 🗂 Logging & Monitoring

All session events are saved in session_logs.jsonl using structured JSON per line:

### ✅ Logged Events
- session_start
- captcha_detected
- captcha_filled
- captcha_loop_detected
- session_terminated (reason: user_closed or normal)
- IP address
- Profile type

### 🔍 Example
```json
{
  "timestamp": "2025-05-29T12:34:56",
  "event": "captcha_filled",
  "message": "Filled with OCR",
  "ip": "123.45.67.89",
  "profile_type": "patchright"
}
```

## 📊 Log Analytics

Run:

```bash
python analyze_logs.py
```

To get metrics per IP + profile group:

- Total sessions
- CAPTCHA solve rate
- CAPTCHA loops
- Average session duration
- Early exits

## 📤 CSV Export

Saved to:

```
session_report.csv
```

With columns:

`ip, profile_type, total_sessions, user_closed, captcha_prompted, captcha_filled, captcha_loops, captcha_solve_rate, captcha_loop_rate, avg_session_duration`

## 🧠 Evasion Techniques

- Patchright (Python): Renders headless Chromium in stealth mode
- OCR Instead of manual CAPTCHA
- Randomized interaction timing
- Avoids automation flags like navigator.webdriver
- Fails gracefully if CAPTCHA loops detected

## 🐍 Run Instructions

### 1. Clone & Install
```bash
git clone <repository-url>
cd irctc-automation

pip install -r requirements.txt
```

Make sure patchright-python is installed:

```bash
pip install patchright
```

You will also need:

- A free API key from https://ocr.space
- Chrome installed on your system (used by Patchright backend)

### 2. Run IRCTC Automation
```bash
python app.py
```

This:

- Opens browser
- Logs in
- Solves CAPTCHA
- Logs session
- Stays active for 180s

### 3. Run Analytics
```bash
python analyze_logs.py
```

Outputs session summary to session_report.csv and prints per-group stats to terminal.

## 📁 New Files Introduced

| File | Description |
|------|-------------|
| session_logs.jsonl | Structured session logs |
| analyze_logs.py | Parses logs, prints report, exports CSV |
| session_report.csv | CSV output of session summary |
| ocr_utils.py | Handles CAPTCHA image preprocessing and OCR |

## ❌ Challenges and Limitations

- **CAPTCHA chaining**: Even with OCR, IRCTC may keep regenerating new CAPTCHAs to trap bots.
- **504 Gateway Errors**: Even with stealth mode, IRCTC may block automation at server level.
- **Dynamic site updates**: XPaths may change, requiring manual updates to the automation script.

## ⏱ Time Spent

Over 8+ hours of development across Python + Patchright integration, stealth patching, CAPTCHA automation, and full-featured logging with analytics.

## 💡 Notes

- No credentials are saved or logged
- Automation is best-effort, with manual fallback
- You can safely observe CAPTCHA behavior and session fingerprinting in action

## 📚 References

- [Patchright Python GitHub](https://github.com/Kaliiiiiiiiii-Vinyzu/patchright)
- [OCR.Space API](https://ocr.space/ocrapi)
- [IRCTC Official](https://www.irctc.co.in/)
