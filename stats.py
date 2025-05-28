# stats.py
from collections import defaultdict
from datetime import datetime
import re

LOG_FILE = "session_stats.log"

def parse_log():
    sessions = []
    current_session = {
        "ip": None,
        "start": None,
        "end": None,
        "success": False,
        "reason": None,
        "captchas": 0,
    }

    with open(LOG_FILE, "r") as f:
        for line in f:
            if "------------------------" in line:
                if current_session["start"]:  # Skip empty session
                    sessions.append(current_session)
                current_session = {
                    "ip": None,
                    "start": None,
                    "end": None,
                    "success": False,
                    "reason": None,
                    "captchas": 0,
                }
                continue

            timestamp_str = line.split(" - ")[0].strip()
            try:
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
            except ValueError:
                continue

            if "Session started" in line:
                current_session["start"] = timestamp
                match = re.search(r"IP: (.+)", line)
                if match:
                    current_session["ip"] = match.group(1)
            elif "CAPTCHA attempt" in line:
                current_session["captchas"] += 1
            elif "Session ended" in line:
                current_session["end"] = timestamp
                current_session["success"] = "Success" in line
                match = re.search(r"Reason: (.+)", line)
                if match:
                    current_session["reason"] = match.group(1)

    return sessions

def show_stats(sessions):
    print(f"Total sessions: {len(sessions)}")
    success_count = sum(1 for s in sessions if s["success"])
    failure_count = len(sessions) - success_count
    print(f"Successful sessions: {success_count}")
    print(f"Failed sessions: {failure_count}")
    
    avg_captcha = sum(s["captchas"] for s in sessions) / len(sessions) if sessions else 0
    print(f"Avg. CAPTCHA attempts per session: {avg_captcha:.2f}")

    ip_count = defaultdict(int)
    for s in sessions:
        ip_count[s["ip"]] += 1
    print("\nSessions per IP:")
    for ip, count in ip_count.items():
        print(f"  {ip}: {count} session(s)")

    print("\nReasons for failure:")
    reasons = defaultdict(int)
    for s in sessions:
        if not s["success"]:
            reasons[s["reason"]] += 1
    for reason, count in reasons.items():
        print(f"  {reason}: {count} time(s)")

def main():
    sessions = parse_log()
    show_stats(sessions)

if __name__ == "__main__":
    main()
