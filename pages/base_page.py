from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    # Common reusable method
    def wait(self):
        return WebDriverWait(self.driver, self.timeout)

    # Webdriver waiting methods
    def wait_for_visiblility(self, locator):
        return self.wait().until(EC.visibility_of_element_located(locator))

    def wait_for_clickable(self, locator):
        return self.wait().until(EC.element_to_be_clickable(locator))

    def wait_for_invisibility(self, locator):
        return self.wait().until(EC.invisibility_of_element_located(locator))

    def wait_for_alert(self):
        return self.wait().until(EC.alert_is_present())

    def wait_for_presence_element(self, locator):
        return self.wait().until(EC.presence_of_element_located(locator))

    def wait_for_presence_of_all_elements(self, locator):
        return self.wait().until(EC.presence_of_all_elements_located(locator))

    # normal method without wait
    def find_element(self, locator):
        return self.driver.find_element(*locator)

    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    # Actions
    def click(self, locator):
        self.wait_for_clickable(locator).click()

    def send_keys(self, locator, value):
        element = self.wait_for_clickable(locator)
        element.clear()
        element.send_keys(value)

    # get methods
    def title(self):
        return self.driver.title

    def text(self, locator):
        return self.wait_for_visiblility(locator).text.strip()

    def get_attribute(self, locator, attribute_name):
        return self.wait_for_visiblility(locator).get_attribute(attribute_name)

    def current_url(self):
        return self.driver.current_url

    # state checkers with proper exception handling
    def is_displayed(self, locator):
        try:
            return self.wait_for_visiblility(locator).is_displayed()
        except TimeoutException:
            return False

    def is_enabled(self, locator):
        try:
            return self.wait_for_visiblility(locator).is_enabled()
        except TimeoutException:
            return False
        

    def is_selected(self, locator):
        try:
            return self.wait_for_presence_element(locator).is_selected()
        except TimeoutException:
            return False


    def select(self, locator):
        if not self.is_selected(locator):
            self.click(locator)
        return self.is_selected(locator)
