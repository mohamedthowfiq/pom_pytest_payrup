from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait


class SignInPage(BasePage):

    #sign in box
    heading_of_signin_box = (By.XPATH,"//h2[text()='Sign in to payRup']")
    sign_in_btn = (By.XPATH,"(//h5[text()='Sign in'])[2]")
    mobile_number_field = (By.XPATH,"//input[@type='number']")
    # VISIBLE clickable element (label/span) - click this
    terms_checkbox_click = (By.XPATH, "//label[contains(@class,'MuiFormControlLabel-root')]/span[1]")
    # HIDDEN input element - use this to check .is_selected()
    terms_checkbox_input = (By.XPATH, "//input[contains(@class,'PrivateSwitchBase-input')]")
    terms_n_conditions_link = (By.XPATH,"//u[text()='terms & conditions']/..")
    get_otp_btn = (By.XPATH,"//button[text()='Get OTP']")

    #verify otp box
    heading_of_otp_box = (By.XPATH, "//h2[text()='Verify OTP']")
    edit_icon = (By.XPATH,"//img[@alt = 'Edit']/..")
    otp_field = (By.XPATH,"//input[@type='number' and contains(@class,'MuiInputBase-input')]")
    def warning_msg(self, message):
            return (By.XPATH,f"//form[contains(@class,'Signin_customform')]//p[normalize-space(text())='{message}']")
    countdown_timer = (By.XPATH,"//b[contains(@class,'Signin_otpText')]") 
    resend_otp = (By.XPATH,"//a[text()='Resend OTP']")
    verify_btn = (By.XPATH,"//button[text()='Verify']")
    
#    Invalid OTP!        OTP sent to your number successfully.
   


    def __init__(self, driver, timeout=10):
        super().__init__(driver, timeout)

    def get_signin_box_heading(self, timeout=10):
        """Return text currently present in the page heading."""
        signin_box_heading = self.text(self.heading_of_signin_box)
        return signin_box_heading

    def click_sign_in_btn(self):
        self.click(self.sign_in_btn)  # going to base_pge.py

    def send_mobile_number(self,mobile_number): # mobile_number is a argument which is expecting value 
        self.send_keys(self.mobile_number_field,mobile_number)# going to base_pge.py

    def get_entered_mobile_number(self):
        """Return text currently present in the mobile number field."""
        return self.get_attribute(self.mobile_number_field,"value")
    
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

    def display_warning_msg(self,message):
        return self.text(self.warning_msg(message)) # going to base_pge.py
    


    # verify otp box

    def get_otp_box_heading(self, timeout=10):
        """Return text currently present in the page heading."""
        otp_box_heading = self.text(self.heading_of_otp_box)
        return otp_box_heading

    def click_edit_icon(self):
        return self.click(self.edit_icon)
    
    def get_entered_otp_number(self):
        """Return text currently present in the otp field.""" 
        return self.get_attribute(self.otp_field,"value")
    

    


    def get_countdown_text(self):
        return self.text(self.countdown_timer)
    

    def countdown_to_seconds(self, time_str):
        minutes, seconds = time_str.split(":")
        return int(minutes) * 60 + int(seconds)


    def get_visible_otp_message(self, timeout=3):
        """
        Returns the currently visible OTP-related message text
        (success / invalid / lock message).
        """
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                lambda d: d.find_elements(
                    By.XPATH,
                    "//form[contains(@class,'Signin_customform')]//p[normalize-space()]"
                )
            )
        except TimeoutException:
            return None

        for el in elements:
            try:
                if el.is_displayed():
                    text = el.text.strip()
                    if text:
                        return text
            except Exception:
                continue

        return None
    