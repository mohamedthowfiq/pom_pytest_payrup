from tests.base_test import BaseTest
from pages.sign_in_page import SignInPage
from utilities.test_data import SignInData,signin_mobile_field__negative_cases
import pytest


class TestSignInPage(BaseTest):

    def setup_sign_in_page(self):
        page = SignInPage(self.driver)
        page.click_sign_in_btn()  # going to sign_in_page
        return page

    def test_valid_sign_in(self):
        sign_in_page = self.setup_sign_in_page()
        sign_in_page.send_mobile_number(SignInData.valid_mobile_number)  # going to sign_in_page
        sign_in_page.check_box_check()  # going to sign_in_page
        sign_in_page.click_get_otp_btn() # going to sign_in_page
        sign_in_page.send_otp(SignInData.static_otp) # going to sign_in_page
        actual_title = sign_in_page.title() # coming from base_page
        expected_title = "Safe & Secure Mobile Recharges & Bill Payment"
        assert actual_title == expected_title,f"Expected title '{expected_title}', but found '{actual_title}'."


    def test_invalid_sign_in(self):
        sign_in_page = self.setup_sign_in_page()
        sign_in_page.send_mobile_number(SignInData.invalid_mobile_number) # going to sign_in_page
        sign_in_page.check_box_check() # going to sign_in_page
        assert  sign_in_page.is_enabled(sign_in_page.get_otp_btn) == False,"Get OTP button should be disabled for invalid mobile number"  # coming from base_page
    



    # 🔽 NEW: one parametrized test for multiple test cases (TC_002–TC_009)
    @pytest.mark.parametrize("tc_id, description, mobile_number, should_enable_otp",
                             signin_mobile_field__negative_cases,
                             ids=[item[0] for item in signin_mobile_field__negative_cases] )
    def test_mobile_number_field_negative_validation(self, tc_id, description, mobile_number, should_enable_otp):
        sign_in_page = self.setup_sign_in_page()
        sign_in_page.send_mobile_number(mobile_number)
        sign_in_page.check_box_check()

         # 🔹 Special validation for TC_005: field must not accept > 10 digits
        if tc_id == "TC_005":
            entered_value = sign_in_page.get_entered_mobile_number()
            assert len(entered_value) == 10, f"{tc_id}: field should only contain 10 digits"
            assert entered_value == mobile_number[:10], (
                f"{tc_id}: field should keep only first 10 digits; "
                f"expected '{mobile_number[:10]}', got '{entered_value}'"
            )
            

         # 🔹 Only check OTP button if we have an expected value (not None)
        if should_enable_otp is not None:
            is_enabled = sign_in_page.is_enabled(sign_in_page.get_otp_btn)

            if should_enable_otp:
                assert is_enabled, f"{tc_id} - {description}: Get OTP button should be ENABLED"
            else:
                assert not is_enabled, f"{tc_id} - {description}: Get OTP button should be DISABLED"
