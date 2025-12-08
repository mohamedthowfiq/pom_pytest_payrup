from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class SignInPage(BasePage):
    sign_in_btn = (By.XPATH,"(//h5[text()='Sign in'])[2]")
    mobile_number_field = (By.XPATH,"//input[@type='number']")
    check_box = (By.XPATH,"//input[@type='checkbox']")
    get_otp_btn = (By.XPATH,"//button[text()='Get OTP']")
    otp_field = (By.XPATH,"//form[contains(@class,'Signin_customform')]//input[@type='number']")
    warning_msg = (By.XPATH,"(//form[contains(@class,'Signin_customform')]//p[2])[1]")

    # def __init__(self, driver, timeout=10):
        # super().__init__(driver, timeout)

    def click_sign_in_btn(self):
        self.click(self.sign_in_btn)  # going to base_pge.py

    def send_mobile_number(self,mobile_number): # mobile_number is a argument which is expecting value 
        self.send_keys(self.mobile_number_field,mobile_number)# going to base_pge.py

    def get_entered_mobile_number(self):
        """Return text currently present in the mobile number field."""
        element = self.driver.find_element(*self.mobile_number_field)
        return element.get_attribute("value")

    def check_box_check(self):
        self.select(self.check_box) # going to base_pge.py
    
    def click_get_otp_btn(self):
        self.click(self.get_otp_btn) # going to base_pge.py
    
    def send_otp(self,otp):
        self.send_keys(self.otp_field,otp) # going to base_pge.py

    def display_warning_msg(self):
        return self.text(self.warning_msg) # going to base_pge.py
    
    
    # def full_sigin_in_page(self,mobile_number,otp):
    #     self.click_sign_in_btn()
    #     self.send_mobile_number(self,mobile_number)
    #     self.check_box_check()
    #     self.click_get_otp_btn()
    #     self.send_otp(self,otp)