import json
from collections import defaultdict
from datetime import datetime

log_file = "session_logs.jsonl"

def parse_logs():
    session_stats = defaultdict(lambda: {
        "total_sessions": 0,
        "user_closed": 0,
        "captcha_prompted": 0,
        "captcha_filled": 0,
        "captcha_loops": 0,
        "session_durations": []
    })

    current_ip = "unknown"
    current_profile = "unknown"
    session_start_time = {}

    with open(log_file, "r") as f:
        for line in f:
            try:
                log = json.loads(line)
            except json.JSONDecodeError:
                continue

            event = log.get("event") or log.get("event_type") or ""

            # Update IP/profile
            if "ip" in log:
                current_ip = log["ip"]
            if "profile_type" in log:
                current_profile = log["profile_type"]

            key = f"{current_ip} | {current_profile}"

            # Parse timestamp
            timestamp_str = log.get("timestamp")
            try:
                timestamp = datetime.fromisoformat(timestamp_str)
            except Exception:
                timestamp = None

            if event == "session_start":
                session_stats[key]["total_sessions"] += 1
                session_start_time[key] = timestamp

            elif event == "captcha_detected":
                session_stats[key]["captcha_prompted"] += 1

            elif event == "captcha_filled":
                session_stats[key]["captcha_filled"] += 1

            elif event == "session_terminated":
                if log.get("reason") == "user_closed":
                    session_stats[key]["user_closed"] += 1

                # Duration tracking
                start_time = session_start_time.get(key)
                if timestamp and start_time:
                    duration = (timestamp - start_time).total_seconds()
                    session_stats[key]["session_durations"].append(duration)

            elif event == "captcha_loop_detected":
                session_stats[key]["captcha_loops"] += 1

    return session_stats

def print_summary(stats):
    print("\n=== IRCTC Session Summary Report ===\n")
    if not stats:
        print("No session data found. Is the log file empty or malformed?")
        return

    for key, data in stats.items():
        duration_list = data["session_durations"]
        avg_duration = sum(duration_list) / len(duration_list) if duration_list else 0

        captcha_prompted = data['captcha_prompted']
        captcha_filled = data['captcha_filled']
        captcha_loops = data['captcha_loops']

        solve_rate = (captcha_filled / captcha_prompted * 100) if captcha_prompted else 0
        loop_rate = (captcha_loops / captcha_prompted * 100) if captcha_prompted else 0

        print(f"Session Group: {key}")
        print(f"  Total Sessions:        {data['total_sessions']}")
        print(f"  User Closed Early:     {data['user_closed']}")
        print(f"  CAPTCHA Prompted:      {captcha_prompted}")
        print(f"  CAPTCHA Filled:        {captcha_filled}")
        print(f"  CAPTCHA Loops Found:   {captcha_loops}")
        print(f"  CAPTCHA Solve Rate:    {solve_rate:.1f}%")
        print(f"  CAPTCHA Loop Rate:     {loop_rate:.1f}%")
        print(f"  Avg. Session Duration: {avg_duration:.2f} sec")
        print("-" * 40)

if __name__ == "__main__":
    stats = parse_logs()
    print_summary(stats)
