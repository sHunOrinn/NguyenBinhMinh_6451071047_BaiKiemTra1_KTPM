"""Lop cha cua moi Page Object: giu driver + bo cho, moi thao tac deu CHO truoc khi lam."""
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import config


class BasePage:
    def __init__(self, driver, timeout: int = config.TIMEOUT):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    # thao tac co cho (Explicit Wait)
    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text: str):
        el = self.find(locator)
        el.clear()
        if text:
            el.send_keys(text)

    def get_attr(self, locator, name: str) -> str:
        return self.find(locator).get_attribute(name) or ""

    # doc trang thai khong can cho
    def is_displayed(self, locator) -> bool:
        return any(el.is_displayed() for el in self.driver.find_elements(*locator))

    def get_url(self) -> str:
        return self.driver.current_url

    def get_title(self) -> str:
        return self.driver.title

    def accept_alert_if_present(self):
        """Dong hop thoai alert (neu co) va tra ve noi dung; khong co thi tra None."""
        try:
            alert = self.driver.switch_to.alert
            text = alert.text
            alert.accept()
            return text
        except NoAlertPresentException:
            return None
