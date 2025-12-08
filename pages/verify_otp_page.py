# pages/verify_otp_page.py
from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class VerifyOtpPage(BasePage):
    # more tolerant xpath (handles extra spaces, etc.)
    heading_of_otp_box = (By.XPATH, "//h2[text()='Verify OTP']")

    def get_page_heading(self, timeout=10):
        """Return text currently present in the page heading."""
        element = self.text(self.heading_of_otp_box)
        return element
