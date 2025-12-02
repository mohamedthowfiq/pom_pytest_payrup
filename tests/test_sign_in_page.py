from tests.base_test import BaseTest
from pages.sign_in_page import SignInPage
from utilities.test_data import TestData


class TestSignInPage(BaseTest):
    def test_valid_sign_in(self):
        sign_in_page  =  SignInPage(self.driver)
        sign_in_page.click_sign_in_btn()
        sign_in_page.send_mobile_number(TestData.mobile_number)
        sign_in_page.check_box_check()
        sign_in_page.click_get_otp_btn()
        sign_in_page.send_otp(TestData.static_otp)
        actual_title = sign_in_page.title()
        expected_title = "Safe & Secure Mobile Recharges & Bill Payment"
        assert actual_title == expected_title,f"Expected title '{expected_title}', but found '{actual_title}'."


    def test_invalid_sign_in(self):
        sign_in_page = SignInPage(self.driver)
        sign_in_page.click_sign_in_btn()
        sign_in_page.send_mobile_number(TestData.invalid_mobile_number)
        sign_in_page.check_box_check()
        assert  sign_in_page.is_enabled(sign_in_page.get_otp_btn) == False,"Get OTP button should be disabled for invalid mobile number"
    
