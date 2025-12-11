from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class SignInPage(BasePage):
    sign_in_btn = (By.XPATH,"(//h5[text()='Sign in'])[2]")
    mobile_number_field = (By.XPATH,"//input[@type='number']")
    # VISIBLE clickable element (label/span) - click this
    terms_checkbox_click = (By.XPATH, "//label[contains(@class,'MuiFormControlLabel-root')]/span[1]")
    # HIDDEN input element - use this to check .is_selected()
    terms_checkbox_input = (By.XPATH, "//input[contains(@class,'PrivateSwitchBase-input')]")
    terms_n_conditions_link = (By.XPATH,"//u[text()='terms & conditions']/..")
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
    
    # ------------------ Clean Checkbox Wrappers ---------------------------------------------------------
    def click_terms_checkbox(self):
        self.click(self.terms_checkbox_click)

    def is_terms_checkbox_selected(self):
        return self.is_selected(self.terms_checkbox_input)

    def ensure_terms_selected(self):
        return self.ensure_state(self.terms_checkbox_click,
                                self.terms_checkbox_input,
                                True)

    def ensure_terms_unselected(self):
        return self.ensure_state(self.terms_checkbox_click,
                                self.terms_checkbox_input,
                                False)
    # -------------------------------------------------------------------------------------------------------
    # backward compatibility for your existing tests
    def check_box_check(self):
        return self.ensure_terms_selected()
    
    def check_is_selected(self):
        """Backwards compatible: return selected status (previously returned nothing)."""
        return self.is_terms_checkbox_selected()
    
    def click_terms_n_conditions_link(self):
        self.click(self.terms_n_conditions_link)

    def click_get_otp_btn(self):
        self.click(self.get_otp_btn) # going to base_pge.py
    
    def send_otp(self,otp):
        self.send_keys(self.otp_field,otp) # going to base_pge.py

    def display_warning_msg(self):
        return self.text(self.warning_msg) # going to base_pge.py
    
    