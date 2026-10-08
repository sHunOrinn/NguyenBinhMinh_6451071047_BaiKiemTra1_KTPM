from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from .base_page import BasePage


class HomePage(BasePage):
    """Trang sau khi dang nhap thanh cong."""

    _password_field = (By.NAME, "userpwd")

    def is_logged_in(self) -> bool:
        """Dang nhap thanh cong = roi khoi /Login va khong con form mat khau."""
        try:
            self.wait.until(lambda d: "/login" not in d.current_url.lower())
        except TimeoutException:
            return False
        return not self.is_displayed(self._password_field)
