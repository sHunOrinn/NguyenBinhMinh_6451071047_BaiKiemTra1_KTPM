from selenium.common.exceptions import TimeoutException

from .base_page import BasePage


class ForgotPasswordPage(BasePage):
    """Trang /Login/GetPass (quen mat khau)."""

    def is_loaded(self) -> bool:
        try:
            self.wait.until(lambda d: "getpass" in d.current_url.lower())
            return True
        except TimeoutException:
            return False

    def go_back(self):
        from .login_page import LoginPage  # import cuc bo de tranh vong lap
        self.driver.back()
        return LoginPage(self.driver)
