from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    #------------------ Wait Helpers -------------
    def wait(self):
        return WebDriverWait(self.driver, self.timeout)

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

    # -------------- normal method without wait -----------
    def find_element(self, locator):
        return self.driver.find_element(*locator)

    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    # ------------------ Basic Actions --------------------
    def click(self, locator):
        self.wait_for_clickable(locator).click()

    def send_keys(self, locator, value):
        element = self.wait_for_clickable(locator)
        element.clear()
        element.send_keys(value)

    # -----------------------  Get Methods ----------------
    def title(self):
        return self.driver.title

    def text(self, locator):
        return self.wait_for_visiblility(locator).text.strip()

    def get_attribute(self, locator, attribute_name):
        return self.wait_for_visiblility(locator).get_attribute(attribute_name)

    def current_url(self):
        return self.driver.current_url
    
    def current_window_handle(self):
        return self.driver.current_window_handle

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
    

    ################################################


    def wait_for_condition(self, condition_callable, timeout=None):
        """Wait until condition_callable(driver) returns truthy."""
        wait_obj = self.wait() if timeout is None else WebDriverWait(self.driver, timeout)
        return wait_obj.until(lambda d: condition_callable(d))

    # ---------------- GENERIC CHECKBOX HANDLER -----------------
    def ensure_state(self, click_locator, state_locator, expected_bool):
        """
        Generic helper: ensure checkbox/toggle reaches expected state (True/False).
        - click_locator → element to click (span/label)
        - state_locator → element whose .is_selected() gives the actual boolean state
        """
        current = self.is_selected(state_locator)

        if current != expected_bool:
            self.click(click_locator)

            # Wait until state updates
            try:
                self.wait().until(
                    lambda d: d.find_element(*state_locator).is_selected() == expected_bool
                )
            except Exception:
                pass  # avoid throwing timeout

        return self.is_selected(state_locator)

