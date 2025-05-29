import asyncio
import datetime
import json
import random
import socket
import sys
import signal

from patchright.async_api import async_playwright
from ocr_utils import solve_captcha_with_ocr_space

from PIL import Image
from io import BytesIO

#Logging Setup#
def get_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        return "unknown"

def log_event(event, message, extra_data=None):
    log_entry = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "event": event,
        "message": message,
        "ip": get_ip(),
        "profile_type": "patchright"
    }
    if extra_data:
        log_entry.update(extra_data)
    with open("session_logs.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

def handle_exit(signum, frame):
    log_event("session_terminated", "Script terminated by user or signal.", {"reason": "user_closed"})
    print("\n--- Session Terminated ---")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

#Automation Script#
async def run():
    log_event("session_start", "Session started.")
    print("[DEBUG] Session started")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--start-maximized"],
            channel="chrome"
        )
        context = await browser.new_context(no_viewport=True)
        page = await context.new_page()

        await page.goto("https://www.irctc.co.in/nget/train-search")
        log_event("navigate", "Navigated to IRCTC website.")
        print("[DEBUG] Navigated to IRCTC homepage")
        await asyncio.sleep(random.uniform(5, 10))

        try:
            login_btn = await page.wait_for_selector("//a[@class='search_btn loginText ng-star-inserted']", timeout=15000)
            await login_btn.click()
            log_event("login_click", "Clicked on Login button.")
            print("[DEBUG] Clicked Login button")
            await asyncio.sleep(random.uniform(5, 7))
        except Exception as e:
            log_event("login_click_fail", f"Failed to click login: {e}")
            print(f"[DEBUG] Login button error: {e}")
            await browser.close()
            return

        try:
            username_field = await page.wait_for_selector('//input[@placeholder="User Name"]', timeout=10000)
            for c in "rajvishwakarma303":
                await username_field.type(c)
                await asyncio.sleep(random.uniform(0.05, 0.15))
            log_event("username_entered", "Username filled.")
            print("[DEBUG] Username entered")

            password_field = await page.wait_for_selector('//input[@placeholder="Password"]', timeout=10000)
            for c in "Raj@321#":
                await password_field.type(c)
                await asyncio.sleep(random.uniform(0.05, 0.15))
            log_event("password_entered", "Password filled.")
            print("[DEBUG] Password entered")

            for attempt in range(3):
                try:
                    captcha_img = await page.wait_for_selector("xpath=/html/body/app-root/app-home/div[3]/app-login/p-dialog[1]/div/div/div[2]/div[2]/div/div[2]/div/div[2]/form/div[5]/div/app-captcha/div/div/div[2]/span[1]/img", timeout=10000)

                    img_bytes = await captcha_img.screenshot()
                    image = Image.open(BytesIO(img_bytes)).convert("RGB")

                    captcha_input = await page.wait_for_selector('//input[@placeholder="Enter Captcha"]', timeout=5000)

                    captcha_text = solve_captcha_with_ocr_space(image, log_event)
                    print(f"[DEBUG] Attempt {attempt+1} - CAPTCHA OCR Output: {captcha_text}")

                    if captcha_text:
                        await captcha_input.click()
                        await asyncio.sleep(0.5)
                        await captcha_input.fill("")
                        for ch in captcha_text:
                            await captcha_input.type(ch)
                            await asyncio.sleep(random.uniform(0.1, 0.2))

                        log_event("captcha_filled_auto", f"Filled CAPTCHA via OCR (Attempt {attempt+1})")
                        print(f"[DEBUG] CAPTCHA filled via OCR (Attempt {attempt+1})")

                        submit_btn = await page.wait_for_selector("xpath=/html/body/app-root/app-home/div[3]/app-login/p-dialog[1]/div/div/div[2]/div[2]/div/div[2]/div/div[2]/form/span/button", timeout=10000)

                        await submit_btn.click()
                        log_event("sign_in_attempt", "Clicked Sign In button")
                        print("[DEBUG] Clicked Sign In button")
                        await asyncio.sleep(5)

                        refreshed_img = await page.wait_for_selector('//img[contains(@src, "captcha")]', timeout=3000)
                        if refreshed_img:
                            new_src = await refreshed_img.get_attribute("src")
                            if new_src != await captcha_img.get_attribute("src"):
                                log_event("captcha_retry", f"CAPTCHA refreshed after submit (Attempt {attempt+1})")
                                print(f"[DEBUG] CAPTCHA refresh detected. Retrying (Attempt {attempt+1})")
                                continue
                            else:
                                break
                    else:
                        log_event("captcha_empty", f"OCR failed on attempt {attempt+1}")
                        print(f"[DEBUG] OCR returned empty or invalid text (Attempt {attempt+1})")
                except Exception as e:
                    log_event("captcha_error", f"Error during CAPTCHA handling (Attempt {attempt+1}): {e}")
                    print(f"[DEBUG] CAPTCHA error on attempt {attempt+1}: {e}")
            else:
                log_event("captcha_manual_required", "OCR failed 3 times. Manual CAPTCHA entry required.")
                print("[DEBUG] CAPTCHA failed 3 times. Manual input may be needed.")

        except Exception as e:
            log_event("form_fill_error", f"Form fill error: {e}")
            print(f"[DEBUG] Form fill error: {e}")
            await browser.close()
            return

        print("--- Login flow complete. Keeping browser open ---")
        await asyncio.sleep(180)
        await browser.close()
        log_event("session_end", "Session ended normally")
        print("[DEBUG] Session ended and browser closed.")

if __name__ == "__main__":
    asyncio.run(run())
