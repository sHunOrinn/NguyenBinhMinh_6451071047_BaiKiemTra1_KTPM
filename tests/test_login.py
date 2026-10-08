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

# test 03
@pytest.mark.tc(
    id='TC03',
    group='Giao diện',
    title='Ô tên đăng nhập: kiểu text, trống mặc định, có gợi ý',
    priority='Trung bình',
    precondition='Chrome đã mở, máy có kết nối Internet.',
    steps=(
        '1. Mở Chrome\n'
        '2. Truy cập https://vanphongdientu.utc.edu.vn/Login\n'
        "3. Kiểm tra ô 'Tên đăng nhập'"
    ),
    data='Không có',
    expected='Ô kiểu text, giá trị rỗng, có placeholder',
)
def test_tc03_o_ten_dang_nhap(driver):
    page = LoginPage(driver).open()
    assert page.get_username_type() == "text"
    assert page.get_username_value() == ""
    assert page.get_username_placeholder().strip() != ""

# test 04
@pytest.mark.tc(
    id='TC04',
    group='Giao diện',
    title='Ô mật khẩu che ký tự khi nhập',
    priority='Cao',
    precondition='Chrome đã mở, máy có kết nối Internet.',
    steps=(
        '1. Mở Chrome\n'
        '2. Truy cập https://vanphongdientu.utc.edu.vn/Login\n'
        "3. Nhập 'Abc@12345' vào ô Mật khẩu"
    ),
    data='Mật khẩu: Abc@12345',
    expected='Ô có type=password (hiển thị dạng chấm) nhưng vẫn nhận đủ dữ liệu',
)
def test_tc04_o_mat_khau_che_ky_tu(driver):
    page = LoginPage(driver).open()
    page.enter_password("Abc@12345")
    assert page.get_password_type() == "password"
    assert page.get_password_value() == "Abc@12345"

# test 05
@pytest.mark.tc(
    id='TC05',
    group='Giao diện',
    title="Nút 'Đăng nhập' hiển thị đúng nhãn và bấm được",
    priority='Trung bình',
    precondition='Chrome đã mở, máy có kết nối Internet.',
    steps=(
        '1. Mở Chrome\n'
        '2. Truy cập https://vanphongdientu.utc.edu.vn/Login\n'
        '3. Kiểm tra nút Đăng nhập'
    ),
    data='Không có',
    expected="Nút có nhãn 'Đăng nhập' và ở trạng thái enabled",
)
def test_tc05_nut_dang_nhap(driver):
    page = LoginPage(driver).open()
    assert "dang nhap" in strip_accents(page.get_login_button_label()).lower()
    assert page.is_login_button_enabled()

# test 06
@pytest.mark.tc(
    id='TC06',
    group='Giao diện',
    title="Ô 'Giữ tôi luôn đăng nhập' mặc định chưa được tick",
    priority='Thấp',
    precondition='Chrome đã mở, máy có kết nối Internet.',
    steps=(
        '1. Mở Chrome\n'
        '2. Truy cập https://vanphongdientu.utc.edu.vn/Login\n'
        "3. Quan sát ô 'Giữ tôi luôn đăng nhập'"
    ),
    data='Không có',
    expected='Ô tick ở trạng thái chưa chọn',
)
def test_tc06_checkbox_mac_dinh(driver):
    page = LoginPage(driver).open()
    assert not page.is_remember_checked()
# test 07
@pytest.mark.tc(
    id='TC07',
    group='Giao diện',
    title="Bấm ô 'Giữ tôi luôn đăng nhập' để tick rồi bỏ tick",
    priority='Trung bình',
    precondition='Chrome đã mở, máy có kết nối Internet.',
    steps=(
        '1. Mở Chrome\n'
        '2. Truy cập https://vanphongdientu.utc.edu.vn/Login\n'
        "3. Bấm vào ô 'Giữ tôi luôn đăng nhập'\n"
        '4. Bấm thêm lần nữa'
    ),
    data='Không có',
    expected='Lần 1: được tick. Lần 2: bỏ tick',
)
def test_tc07_checkbox_tick_bo_tick(driver):
    page = LoginPage(driver).open()
    page.toggle_remember()
    assert page.is_remember_checked(), "Sau lần bấm 1 phải được tick"
    page.toggle_remember()
    assert not page.is_remember_checked(), "Sau lần bấm 2 phải bỏ tick"
# test 08
@pytest.mark.tc(
    id='TC08',
    group='Giao diện',
    title='Phím Tab chuyển focus từ ô tên đăng nhập sang ô mật khẩu',
    priority='Thấp',
    precondition='Chrome đã mở, máy có kết nối Internet.',
    steps=(
        '1. Mở Chrome\n'
        '2. Truy cập https://vanphongdientu.utc.edu.vn/Login\n'
        '3. Bấm vào ô Tên đăng nhập\n'
        '4. Nhấn phím Tab'
    ),
    data='Không có',
    expected='Focus chuyển sang ô Mật khẩu',
)
def test_tc08_phim_tab_chuyen_o(driver):
    page = LoginPage(driver).open()
    page.focus_username()
    assert page.focused_field_name() == "username"
    page.press_tab()
    assert page.focused_field_name() == "userpwd"
# test 09
@pytest.mark.tc(
    id='TC09',
    group='Giao diện',
    title='Giao diện điện thoại (375x812): vẫn thấy form đăng nhập',
    priority='Trung bình',
    precondition='Chrome đã mở, máy có kết nối Internet.',
    steps=(
        '1. Mở Chrome, thu cửa sổ về 375x812\n'
        '2. Truy cập https://vanphongdientu.utc.edu.vn/Login'
    ),
    data='Kích thước: 375x812',
    expected='Ô tên đăng nhập, ô mật khẩu và nút Đăng nhập vẫn hiển thị',
)
def test_tc09_giao_dien_mobile(driver):
    driver.set_window_size(375, 812)
    page = LoginPage(driver).open()
    assert page.core_form_visible()
# test 10

# test 11

# test 12

# test 13

