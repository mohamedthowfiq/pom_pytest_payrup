from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class SignInPage(BasePage):
    sign_in_btn = (By.XPATH,"(//h5[text()='Sign in'])[2]")
    mobile_number_field = (By.XPATH,"//input[@type='number']")
    # check_box = (By.XPATH,"//label[contains(@class,'MuiFormControlLabel-root')]/span[1]").
    # VISIBLE clickable element (label/span) - click this
    terms_checkbox_click = (By.XPATH, "//label[contains(@class,'MuiFormControlLabel-root')]/span[1]")
    # HIDDEN input element - use this to check .is_selected()
    terms_checkbox_input = (By.XPATH, "//input[contains(@class,'PrivateSwitchBase-input')]")
    get_otp_btn = (By.XPATH,"//button[text()='Get OTP']")
    otp_field = (By.XPATH,"//form[contains(@class,'Signin_customform')]//input[@type='number']")
    warning_msg = (By.XPATH,"(//form[contains(@class,'Signin_customform')]//p[2])[1]")

    def __init__(self, driver, timeout=10):
        super().__init__(driver, timeout)

    def click_sign_in_btn(self):
        self.click(self.sign_in_btn)  # going to base_pge.py

    def send_mobile_number(self,mobile_number): # mobile_number is a argument which is expecting value 
        self.send_keys(self.mobile_number_field,mobile_number)# going to base_pge.py

    def get_entered_mobile_number(self):
        """Return text currently present in the mobile number field."""
        element = self.driver.find_element(*self.mobile_number_field)
        return element.get_attribute("value")
    
    # ------------------ checkbox helpers ---------------------------------------------------------
    def click_terms_checkbox(self):
        """Click the visible element (label/span) to toggle the checkbox."""
        self.click(self.terms_checkbox_click)

    def is_terms_checkbox_selected(self):
        """Return True/False reading the hidden input's checked state."""
        return self.is_selected(self.terms_checkbox_input)

    def ensure_terms_checkbox_selected(self):
        """Convenience: ensure checkbox is checked, return final boolean."""
        if not self.is_terms_checkbox_selected():
            self.click_terms_checkbox()
            # small wait for state to update (optional)
            try:
                # use the BasePage wait utilities if you added wait_for_presence_element
                self.wait().until(lambda d: d.find_element(*self.terms_checkbox_input).is_selected())
            except Exception:
                pass
        return self.is_terms_checkbox_selected()

    def ensure_terms_checkbox_unselected(self):
        """Convenience: ensure checkbox is unchecked, return final boolean."""
        if self.is_terms_checkbox_selected():
            self.click_terms_checkbox()
            try:
                self.wait().until(lambda d: not d.find_element(*self.terms_checkbox_input).is_selected())
            except Exception:
                pass
        return not self.is_terms_checkbox_selected()
    # -------------------------------------------------------------------------------------------------------

    # def check_box_check(self):
    #     self.select(self.ensure_terms_checkbox_selected) 
    def check_box_check(self):
        """Backwards compatible: existing tests call this to toggle/ensure selected."""
        return self.ensure_terms_checkbox_selected()
    
    # def check_is_selected(self):
    #     self.is_selected(self.check_box)
    
    def check_is_selected(self):
        """Backwards compatible: return selected status (previously returned nothing)."""
        return self.is_terms_checkbox_selected()
    
    def click_get_otp_btn(self):
        self.click(self.get_otp_btn) # going to base_pge.py
    
    def send_otp(self,otp):
        self.send_keys(self.otp_field,otp) # going to base_pge.py

    def display_warning_msg(self):
        return self.text(self.warning_msg) # going to base_pge.py
    
    