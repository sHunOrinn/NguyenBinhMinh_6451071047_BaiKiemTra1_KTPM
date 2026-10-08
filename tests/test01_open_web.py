import pytest
from utils.text import strip_accents
from pages.login_page import LoginPage


@pytest.mark.tc(
    id='TC01',
    group='Giao diện',
    title='Mở trang đăng nhập: URL, tiêu đề, HTTPS',
    priority='Cao',
    precondition='Chrome đã mở, máy có kết nối Internet.',
    steps=(
        '1. Mở Chrome\n'
        '2. Truy cập https://vanphongdientu.utc.edu.vn/Login'
    ),
    data='Không có',
    expected="Trang tải thành công qua HTTPS, URL chứa /Login, tiêu đề có chữ 'Đăng nhập'",
)
def test_tc01_mo_trang_dang_nhap(driver):
    page = LoginPage(driver).open()
    assert page.get_url().startswith("https://"), "Trang không dùng HTTPS"
    assert page.is_on_login_page()
    assert "dang nhap" in strip_accents(page.get_title()).lower()
