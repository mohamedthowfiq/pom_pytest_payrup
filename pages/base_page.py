from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

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
    






    # common backdrop locator used by Material UI modals
    BACKDROP = (By.CSS_SELECTOR, ".MuiBackdrop-root")

    def wait_for_invisibility_of_backdrop(self, timeout=3):
        """Wait a short while for the common modal/backdrop to disappear (if present)."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(self.BACKDROP))
        except TimeoutException:
            # if still present after short wait, continue — safe_click will attempt JS fallback
            pass

    # convenience aliases that tests sometimes call
    def find(self, locator, timeout=None):
        """Return first element presence (alias used in tests)."""
        if timeout is None:
            return self.wait_for_presence_element(locator)
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))

    def find_visible(self, locator, timeout=None):
        """Return first visible element (alias)."""
        if timeout is None:
            return self.wait_for_visiblility(locator)
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def is_visible(self, locator, timeout=2):
        try:
            self.find_visible(locator, timeout)
            return True
        except TimeoutException:
            return False

    def safe_click(self, locator, timeout=10):
        """
        Robust click:
        - wait for common backdrops to vanish
        - wait element to be clickable
        - try native click, otherwise JS click
        """
        # short wait for backdrop/overlay to disappear first
        self.wait_for_invisibility_of_backdrop(timeout=2)

        try:
            el = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
            try:
                el.click()
                return
            except WebDriverException:
                # native click failed (maybe overlay appeared) -> fallback to JS click
                self.driver.execute_script("arguments[0].click();", el)
                return
        except Exception:
            # last resort: try to find element and JS-click it (keeps tests resilient)
            try:
                el = self.find(locator, timeout=2)
                self.driver.execute_script("arguments[0].click();", el)
            except Exception:
                raise  # re-raise so test fails loudly if truly not clickable

