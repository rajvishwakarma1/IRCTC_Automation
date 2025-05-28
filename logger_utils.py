# logger_utils.py
import logging
import os
import csv
from datetime import datetime
import requests

os.makedirs("logs", exist_ok=True)

def setup_logger():
    logging.basicConfig(
        filename=f'logs/session_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(message)s'
    )

def get_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except Exception:
        return "IP fetch error"

def log_result_csv(status, profile_type="clean", ip="unknown"):
    file_path = 'logs/results.csv'
    file_exists = os.path.exists(file_path)
    with open(file_path, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "status", "profile_type", "ip"])
        writer.writerow([datetime.now(), status, profile_type, ip])
