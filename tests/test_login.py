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
@pytest.mark.tc(
    id='TC10',
    group='Giao diện',
    title='Trang đăng nhập tải xong trong 10 giây',
    priority='Thấp',
    precondition='Chrome đã mở, máy có kết nối Internet.',
    steps=(
        '1. Mở Chrome\n'
        '2. Truy cập https://vanphongdientu.utc.edu.vn/Login\n'
        '3. Đo thời gian từ lúc truy cập đến khi thấy ô tên đăng nhập'
    ),
    data='Ngưỡng: 10 giây',
    expected='Thời gian tải < 10 giây',
)
def test_tc10_thoi_gian_tai_trang(driver):
    start = time.perf_counter()
    LoginPage(driver).open()
    elapsed = time.perf_counter() - start
    assert elapsed < 10, f"Trang tải mất {elapsed:.1f}s (ngưỡng 10s)"

# test 11
@pytest.mark.tc(
    id='TC11',
    group='Validate – tiêu cực',
    title='Để trống cả tên đăng nhập và mật khẩu',
    priority='Cao',
    precondition='Chrome đã mở, máy có kết nối Internet.',
    steps=(
        '1. Mở Chrome\n'
        '2. Truy cập https://vanphongdientu.utc.edu.vn/Login\n'
        '3. Nhập tên đăng nhập: (để trống)\n'
        '4. Nhập mật khẩu: (để trống)\n'
        "5. Bấm nút 'Đăng nhập'"
    ),
    data='Cả hai ô để trống',
    expected='Không đăng nhập được, vẫn ở trang đăng nhập và còn form đăng nhập',
)
def test_tc11_de_trong_ca_hai(driver):
    page = LoginPage(driver).open()
    page.attempt_login("", "")
    assert page.login_rejected(), "Phải ở lại trang đăng nhập"
# test 12
@pytest.mark.tc(
    id='TC12',
    group='Validate – tiêu cực',
    title='Để trống tên đăng nhập, có nhập mật khẩu',
    priority='Cao',
    precondition='Chrome đã mở, máy có kết nối Internet.',
    steps=(
        '1. Mở Chrome\n'
        '2. Truy cập https://vanphongdientu.utc.edu.vn/Login\n'
        '3. Nhập tên đăng nhập: (để trống)\n'
        '4. Nhập mật khẩu: Abc@12345\n'
        "5. Bấm nút 'Đăng nhập'"
    ),
    data='Mật khẩu: Abc@12345',
    expected='Không đăng nhập được, vẫn ở trang đăng nhập và còn form đăng nhập',
)
def test_tc12_de_trong_ten_dang_nhap(driver):
    page = LoginPage(driver).open()
    page.attempt_login("", "Abc@12345")
    assert page.login_rejected(), "Phải ở lại trang đăng nhập"
# test 13
@pytest.mark.tc(
    id='TC13',
    group='Validate – tiêu cực',
    title='Có tên đăng nhập, để trống mật khẩu',
    priority='Cao',
    precondition='Chrome đã mở, máy có kết nối Internet.',
    steps=(
        '1. Mở Chrome\n'
        '2. Truy cập https://vanphongdientu.utc.edu.vn/Login\n'
        '3. Nhập tên đăng nhập: sinhvien_tc13\n'
        '4. Nhập mật khẩu: (để trống)\n'
        "5. Bấm nút 'Đăng nhập'"
    ),
    data='Tên đăng nhập: sinhvien_tc13',
    expected='Không đăng nhập được, vẫn ở trang đăng nhập và còn form đăng nhập',
)
def test_tc13_de_trong_mat_khau(driver):
    page = LoginPage(driver).open()
    page.attempt_login("sinhvien_tc13", "")
    assert page.login_rejected(), "Phải ở lại trang đăng nhập"

# test 14
@pytest.mark.tc(
    id='TC14',
    group='Validate – tiêu cực',
    title='Tên đăng nhập không tồn tại',
    priority='Cao',
    precondition='Chrome đã mở, máy có kết nối Internet.',
    steps=(
        '1. Mở Chrome\n'
        '2. Truy cập https://vanphongdientu.utc.edu.vn/Login\n'
        '3. Nhập tên đăng nhập: khong_ton_tai_tc14\n'
        '4. Nhập mật khẩu: Sai@Pass123\n'
        "5. Bấm nút 'Đăng nhập'"
    ),
    data='Tên đăng nhập: khong_ton_tai_tc14; Mật khẩu: Sai@Pass123',
    expected='Không đăng nhập được, vẫn ở trang đăng nhập và còn form đăng nhập',
)
def test_tc14_tai_khoan_khong_ton_tai(driver):
    page = LoginPage(driver).open()
    page.attempt_login("khong_ton_tai_tc14", "Sai@Pass123")
    assert page.login_rejected(), "Phải ở lại trang đăng nhập"

# test 15
@pytest.mark.tc(
    id='TC15',
    group='Validate – tiêu cực',
    title='Đúng tên đăng nhập, sai mật khẩu',
    priority='Cao',
    precondition='Chrome đã mở, có Internet; đã khai báo UTC_USER/UTC_PASS (tài khoản thử nghiệm) trong file .env.',
    steps=(
        '1. Mở Chrome\n'
        '2. Truy cập https://vanphongdientu.utc.edu.vn/Login\n'
        '3. Nhập tên đăng nhập: (tài khoản hợp lệ)\n'
        "4. Nhập mật khẩu: (mật khẩu hợp lệ + '_sai')\n"
        "5. Bấm nút 'Đăng nhập'"
    ),
    data="Tài khoản hợp lệ lấy từ file .env; mật khẩu thêm hậu tố '_sai'",
    expected='Không đăng nhập được, vẫn ở trang đăng nhập và còn form đăng nhập',
)
@requires_credentials
def test_tc15_dung_tai_khoan_sai_mat_khau(driver):
    page = LoginPage(driver).open()
    page.attempt_login(config.UTC_USER, config.UTC_PASS + "_sai")
    assert page.login_rejected(), "Phải ở lại trang đăng nhập"

# test 16
@pytest.mark.tc(
    id='TC16',
    group='Validate – tiêu cực',
    title='Sai tên đăng nhập, đúng mật khẩu',
    priority='Trung bình',
    precondition='Chrome đã mở, có Internet; đã khai báo UTC_USER/UTC_PASS (tài khoản thử nghiệm) trong file .env.',
    steps=(
        '1. Mở Chrome\n'
        '2. Truy cập https://vanphongdientu.utc.edu.vn/Login\n'
        "3. Nhập tên đăng nhập: (tài khoản hợp lệ + '_x9')\n"
        '4. Nhập mật khẩu: (mật khẩu hợp lệ)\n'
        "5. Bấm nút 'Đăng nhập'"
    ),
    data="Tài khoản hợp lệ lấy từ file .env; tên đăng nhập thêm hậu tố '_x9'",
    expected='Không đăng nhập được, vẫn ở trang đăng nhập và còn form đăng nhập',
)
@requires_credentials
def test_tc16_sai_tai_khoan_dung_mat_khau(driver):
    page = LoginPage(driver).open()
    page.attempt_login(config.UTC_USER + "_x9", config.UTC_PASS)
    assert page.login_rejected(), "Phải ở lại trang đăng nhập"

# test 17
@pytest.mark.tc(
    id='TC17',
    group='Validate – tiêu cực',
    title='Mật khẩu phân biệt chữ hoa/thường',
    priority='Trung bình',
    precondition='Chrome đã mở, có Internet; đã khai báo UTC_USER/UTC_PASS (tài khoản thử nghiệm) trong file .env.',
    steps=(
        '1. Mở Chrome\n'
        '2. Truy cập https://vanphongdientu.utc.edu.vn/Login\n'
        '3. Nhập tên đăng nhập: (tài khoản hợp lệ)\n'
        '4. Nhập mật khẩu: (mật khẩu hợp lệ đảo hoa/thường)\n'
        "5. Bấm nút 'Đăng nhập'"
    ),
    data='Tài khoản hợp lệ lấy từ file .env; mật khẩu đảo hoa/thường (swapcase)',
    expected='Không đăng nhập được, vẫn ở trang đăng nhập và còn form đăng nhập',
)
@requires_credentials
def test_tc17_mat_khau_phan_biet_hoa_thuong(driver):
    if config.UTC_PASS.swapcase() == config.UTC_PASS:
        pytest.skip("Mật khẩu không có chữ cái nên không thể đảo hoa/thường")
    page = LoginPage(driver).open()
    page.attempt_login(config.UTC_USER, config.UTC_PASS.swapcase())
    assert page.login_rejected(), "Phải ở lại trang đăng nhập"

# test 18
@pytest.mark.tc(
    id='TC18',
    group='Validate – tiêu cực',
    title='Chỉ nhập khoảng trắng vào cả hai ô',
    priority='Trung bình',
    precondition='Chrome đã mở, máy có kết nối Internet.',
    steps=(
        '1. Mở Chrome\n'
        '2. Truy cập https://vanphongdientu.utc.edu.vn/Login\n'
        "3. Nhập tên đăng nhập: '   '\n"
        "4. Nhập mật khẩu: '   '\n"
        "5. Bấm nút 'Đăng nhập'"
    ),
    data='3 dấu cách ở mỗi ô',
    expected='Không đăng nhập được, vẫn ở trang đăng nhập và còn form đăng nhập',
)
def test_tc18_chi_khoang_trang(driver):
    page = LoginPage(driver).open()
    page.attempt_login("   ", "   ")
    assert page.login_rejected(), "Phải ở lại trang đăng nhập"

# test 19
@pytest.mark.tc(
    id='TC19',
    group='Validate – tiêu cực',
    title='Nhập chuỗi rất dài (500 ký tự)',
    priority='Thấp',
    precondition='Chrome đã mở, máy có kết nối Internet.',
    steps=(
        '1. Mở Chrome\n'
        '2. Truy cập https://vanphongdientu.utc.edu.vn/Login\n'
        "3. Nhập tên đăng nhập: 'a' x 500\n"
        "4. Nhập mật khẩu: 'b' x 500\n"
        "5. Bấm nút 'Đăng nhập'"
    ),
    data="500 ký tự 'a' và 500 ký tự 'b'",
    expected='Không đăng nhập được, trang không lỗi/treo, vẫn ở trang đăng nhập',
)
def test_tc19_chuoi_qua_dai(driver):
    page = LoginPage(driver).open()
    page.attempt_login("a" * 500, "b" * 500)
    assert page.login_rejected(), "Phải ở lại trang đăng nhập"

# test 20
@pytest.mark.tc(
    id='TC20',
    group='Validate – tiêu cực',
    title='Ký tự đặc biệt / chuỗi kiểu SQL injection không qua được đăng nhập',
    priority='Cao',
    precondition='Chrome đã mở, máy có kết nối Internet.',
    steps=(
        '1. Mở Chrome\n'
        '2. Truy cập https://vanphongdientu.utc.edu.vn/Login\n'
        "3. Nhập tên đăng nhập: ' OR '1'='1' --\n"
        "4. Nhập mật khẩu: ' OR '1'='1' --\n"
        "5. Bấm nút 'Đăng nhập'"
    ),
    data="Chuỗi: ' OR '1'='1' --",
    expected='Không đăng nhập được, không hiện lỗi máy chủ',
)
def test_tc20_ky_tu_dac_biet_sqli(driver):
    page = LoginPage(driver).open()
    page.attempt_login("' OR '1'='1' --", "' OR '1'='1' --")
    assert page.login_rejected(), "Phải ở lại trang đăng nhập"
    assert "server error" not in driver.page_source.lower()

# test 21
@pytest.mark.tc(
    id='TC21',
    group='Validate – tiêu cực',
    title='Chèn thẻ <script> vào ô nhập không bị thực thi',
    priority='Cao',
    precondition='Chrome đã mở, máy có kết nối Internet.',
    steps=(
        '1. Mở Chrome\n'
        '2. Truy cập https://vanphongdientu.utc.edu.vn/Login\n'
        "3. Nhập tên đăng nhập: <script>alert('xss')</script>\n"
        '4. Nhập mật khẩu: Abc@12345\n'
        "5. Bấm nút 'Đăng nhập'"
    ),
    data="Chuỗi: <script>alert('xss')</script>",
    expected="Script không chạy (không có alert 'xss'), vẫn ở trang đăng nhập",
)
def test_tc21_chen_script_xss(driver):
    page = LoginPage(driver).open()
    page.attempt_login("<script>alert('xss')</script>", "Abc@12345")
    assert page.login_rejected(), "Phải ở lại trang đăng nhập"
    assert page.last_alert_text != "xss", "Mã script đã bị thực thi!"

# test 22
@pytest.mark.tc(
    id='TC22',
    group='Validate – tiêu cực',
    title='Nhập tiếng Việt có dấu và ký tự lạ',
    priority='Thấp',
    precondition='Chrome đã mở, máy có kết nối Internet.',
    steps=(
        '1. Mở Chrome\n'
        '2. Truy cập https://vanphongdientu.utc.edu.vn/Login\n'
        '3. Nhập tên đăng nhập: Nguyễn Văn Ạ ★\n'
        '4. Nhập mật khẩu: Mật@khẩu★123\n'
        "5. Bấm nút 'Đăng nhập'"
    ),
    data='Tên: Nguyễn Văn Ạ ★; Mật khẩu: Mật@khẩu★123',
    expected='Không đăng nhập được, trang không lỗi',
)
def test_tc22_tieng_viet_ky_tu_la(driver):
    page = LoginPage(driver).open()
    page.attempt_login("Nguyễn Văn Ạ ★", "Mật@khẩu★123")
    assert page.login_rejected(), "Phải ở lại trang đăng nhập"

# test 23
@pytest.mark.tc(
    id='TC23',
    group='Đăng nhập – tích cực',
    title='Đăng nhập thành công bằng tài khoản hợp lệ',
    priority='Cao',
    precondition='Chrome đã mở, có Internet; đã khai báo UTC_USER/UTC_PASS (tài khoản thử nghiệm) trong file .env.',
    steps=(
        '1. Mở Chrome\n'
        '2. Truy cập https://vanphongdientu.utc.edu.vn/Login\n'
        '3. Nhập tên đăng nhập và mật khẩu hợp lệ\n'
        "4. Bấm nút 'Đăng nhập'"
    ),
    data='Tài khoản hợp lệ lấy từ file .env',
    expected='Rời khỏi trang /Login và không còn form đăng nhập',
)
@requires_credentials
def test_tc23_dang_nhap_thanh_cong(driver):
    home = LoginPage(driver).open().login_as(config.UTC_USER, config.UTC_PASS)
    assert home.is_logged_in(), "Đăng nhập không thành công"

# test 24
@pytest.mark.tc(
    id='TC24',
    group='Đăng nhập – tích cực',
    title='Đăng nhập thành công bằng phím Enter',
    priority='Trung bình',
    precondition='Chrome đã mở, có Internet; đã khai báo UTC_USER/UTC_PASS (tài khoản thử nghiệm) trong file .env.',
    steps=(
        '1. Mở Chrome\n'
        '2. Truy cập https://vanphongdientu.utc.edu.vn/Login\n'
        '3. Nhập tên đăng nhập và mật khẩu hợp lệ\n'
        '4. Đặt con trỏ ở ô Mật khẩu rồi nhấn Enter'
    ),
    data='Tài khoản hợp lệ lấy từ file .env',
    expected='Form được gửi đi và đăng nhập thành công',
)
@requires_credentials
def test_tc24_dang_nhap_bang_phim_enter(driver):
    page = LoginPage(driver).open()
    page.enter_username(config.UTC_USER)
    page.enter_password(config.UTC_PASS)
    page.submit_with_enter()
    assert HomePage(driver).is_logged_in(), "Nhấn Enter không đăng nhập được"

