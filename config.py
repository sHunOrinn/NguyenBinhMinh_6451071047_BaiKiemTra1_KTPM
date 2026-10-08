"""Cau hinh trung tam. Tai khoan that doc tu file .env / bien moi truong, KHONG viet vao code."""
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:  # chua cai python-dotenv thi van dung duoc bien moi truong
    pass

BASE_URL = "https://vanphongdientu.utc.edu.vn"
LOGIN_URL = f"{BASE_URL}/Login"
FORGOT_URL = f"{BASE_URL}/Login/GetPass"

UTC_USER = os.getenv("UTC_USER") or None
UTC_PASS = os.getenv("UTC_PASS") or None
HAS_CREDENTIALS = bool(UTC_USER and UTC_PASS)

HEADLESS = os.getenv("HEADLESS", "0") == "1"
TIMEOUT = int(os.getenv("TIMEOUT", "10"))
