from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import config
from .base_page import BasePage
from .forgot_password_page import ForgotPasswordPage
from .home_page import HomePage


class LoginPage(BasePage):
    URL = config.LOGIN_URL

    # locator (private)
    _username = (By.NAME, "username")
    _password = (By.NAME, "userpwd")
    _remember_input = (By.ID, "persistent")                # o that bi JS an: CHI de doc isSelected()
    _remember_label = (By.CSS_SELECTOR, "label.check")     # o hien thi: dung de click
    _login_btn = (By.CSS_SELECTOR, "input.submit_login")
    _google_btn = (By.XPATH, "//a[contains(text(),'e-mail UTC')]")
    _forgot_link = (By.CSS_SELECTOR, "a[href='/Login/GetPass']")
    _help_link = (By.CSS_SELECTOR, "a[href*='hotrokythuat.utc.edu.vn']")
    _feedback_link = (By.CSS_SELECTOR, "a[href^='mailto:']")

    def __init__(self, driver, timeout: int = config.TIMEOUT):
        super().__init__(driver, timeout)
        self.last_alert_text = None   # noi dung alert (neu trang bao loi bang alert)

    # dieu huong
    def open(self):
        self.driver.get(self.URL)
        self.find(self._username)
        return self

    def is_on_login_page(self) -> bool:
        return "/login" in self.driver.current_url.lower()

    def has_login_form(self) -> bool:
        return self.is_displayed(self._password) and self.is_displayed(self._login_btn)

    def wait_until_login_form(self) -> bool:
        try:
            self.find(self._password)
            return True
        except TimeoutException:
            return False

    def login_rejected(self) -> bool:
        """Dang nhap bi tu choi = van o /Login va van thay form dang nhap."""
        return self.is_on_login_page() and self.has_login_form()

    # nhap lieu
    def enter_username(self, text: str):
        self.type(self._username, text)

    def enter_password(self, text: str):
        self.type(self._password, text)

    def get_username_value(self) -> str:
        return self.get_attr(self._username, "value")

    def get_password_value(self) -> str:
        return self.get_attr(self._password, "value")

    def get_username_type(self) -> str:
        return self.get_attr(self._username, "type")

    def get_password_type(self) -> str:
        return self.get_attr(self._password, "type")

    def get_username_placeholder(self) -> str:
        return self.get_attr(self._username, "placeholder")

    def get_login_button_label(self) -> str:
        return self.get_attr(self._login_btn, "value")   # <input type=submit>: chu nam o value

    def is_login_button_enabled(self) -> bool:
        return self.find(self._login_btn).is_enabled()

    # checkbox "Giu toi luon dang nhap"
    def is_remember_checked(self) -> bool:
        return self.driver.find_element(*self._remember_input).is_selected()

    def toggle_remember(self):
        self.click(self._remember_label)

    # ban phim
    def focus_username(self):
        self.click(self._username)

    def press_tab(self):
        self.driver.switch_to.active_element.send_keys(Keys.TAB)

    def focused_field_name(self) -> str:
        return self.driver.switch_to.active_element.get_attribute("name") or ""

    # gui form
    def _wait_submit_result(self, old_element):
        """Cho toi khi: co alert / roi /Login / trang tai lai (phan tu cu bi stale).
        Het 4s khong co gi -> form bi chan o phia trinh duyet (validation), khong loi."""
        def done(d):
            try:
                _ = d.switch_to.alert
                return True
            except NoAlertPresentException:
                pass
            if "/login" not in d.current_url.lower():
                return True
            return EC.staleness_of(old_element)(d)

        try:
            WebDriverWait(self.driver, 4).until(done)
        except TimeoutException:
            pass
        self.last_alert_text = self.accept_alert_if_present()

    def submit(self):
        old = self.find(self._login_btn)
        self.click(self._login_btn)
        self._wait_submit_result(old)

    def submit_with_enter(self):
        old = self.find(self._login_btn)
        self.driver.find_element(*self._password).send_keys(Keys.ENTER)
        self._wait_submit_result(old)

    def attempt_login(self, username: str, password: str):
        """Dang nhap voi y dinh THAT BAI / kiem tra validation -> o lai trang nay."""
        self.enter_username(username)
        self.enter_password(password)
        self.submit()
        return self

    def login_as(self, username: str, password: str) -> HomePage:
        """Dang nhap voi y dinh THANH CONG -> tra ve HomePage (Fluent Navigation)."""
        self.attempt_login(username, password)
        return HomePage(self.driver)

    # trang thai thanh phan
    def main_elements_status(self) -> dict:
        return {
            "O ten dang nhap": self.is_displayed(self._username),
            "O mat khau": self.is_displayed(self._password),
            "O tick Giu toi luon dang nhap": self.is_displayed(self._remember_label),
            "Nut Dang nhap": self.is_displayed(self._login_btn),
            "Nut Dang nhap bang e-mail UTC": self.is_displayed(self._google_btn),
            "Link Quen mat khau": self.is_displayed(self._forgot_link),
            "Link Trung tam tro giup": self.is_displayed(self._help_link),
            "Link Y kien phan hoi": self.is_displayed(self._feedback_link),
        }

    def core_form_visible(self) -> bool:
        return (self.is_displayed(self._username)
                and self.is_displayed(self._password)
                and self.is_displayed(self._login_btn))

    # cac lien ket
    def click_forgot_password(self) -> ForgotPasswordPage:
        self.click(self._forgot_link)
        return ForgotPasswordPage(self.driver)

    def click_google_login(self) -> str:
        """Bam 'Dang nhap bang e-mail UTC' va tra ve URL dich (khong nhap gi tren Google)."""
        self.click(self._google_btn)
        try:
            WebDriverWait(self.driver, 15).until(
                lambda d: "accounts.google.com" in d.current_url)
        except TimeoutException:
            pass
        return self.driver.current_url

    def open_help_center(self):
        """Bam 'Trung tam tro giup' (mo tab moi). Tra ve (so tab, URL tab moi), roi dong tab moi."""
        main = self.driver.current_window_handle
        self.click(self._help_link)
        try:
            WebDriverWait(self.driver, 10).until(EC.number_of_windows_to_be(2))
        except TimeoutException:
            pass
        handles = self.driver.window_handles
        new_tabs = [h for h in handles if h != main]
        if new_tabs:
            self.driver.switch_to.window(new_tabs[0])
            WebDriverWait(self.driver, 15).until(
                lambda d: d.current_url not in ("", "about:blank", "data:,"))
        url = self.driver.current_url
        count = len(handles)
        if new_tabs:
            self.driver.close()
            self.driver.switch_to.window(main)
        return count, url

    def get_feedback_href(self) -> str:
        return self.driver.find_element(*self._feedback_link).get_attribute("href") or ""
