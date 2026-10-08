import time

import pytest

import config
from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.markers import requires_credentials
from utils.text import strip_accents

# test 01
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

# test 02
@pytest.mark.tc(
    id='TC02',
    group='Giao diện',
    title='Hiển thị đầy đủ các thành phần trên trang đăng nhập',
    priority='Cao',
    precondition='Chrome đã mở, máy có kết nối Internet.',
    steps=(
        '1. Mở Chrome\n'
        '2. Truy cập https://vanphongdientu.utc.edu.vn/Login\n'
        '3. Quan sát các thành phần'
    ),
    data='Không có',
    expected="Thấy đủ: ô tên đăng nhập, ô mật khẩu, ô tick 'Giữ tôi luôn đăng nhập', nút Đăng nhập, nút đăng nhập e-mail UTC, link Quên mật khẩu, Trung tâm trợ giúp, Ý kiến phản hồi",
)
def test_tc02_day_du_thanh_phan(driver):
    page = LoginPage(driver).open()
    missing = [name for name, shown in page.main_elements_status().items() if not shown]
    assert not missing, f"Thiếu hoặc bị ẩn: {missing}"

