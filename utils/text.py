import unicodedata


def strip_accents(text: str) -> str:
    """'Đăng nhập' -> 'Dang nhap' (so sanh khong phu thuoc dau tieng Viet)."""
    text = (text or "").replace("đ", "d").replace("Đ", "D")
    normalized = unicodedata.normalize("NFD", text)
    return "".join(c for c in normalized if unicodedata.category(c) != "Mn")
