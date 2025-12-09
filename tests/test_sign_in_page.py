from tests.base_test import BaseTest
from pages.sign_in_page import SignInPage
from pages.verify_otp_page import VerifyOtpPage
from utilities.test_data import SignInData,\
                    signin_mobile_field__negative_cases,\
                    signin_mobile_field__positive_cases,\
                    terms_checkbox_cases,\
                    terms_link_cases,\
                    terms_get_otp_cases
import pytest


class TestSignInPage(BaseTest):

    def setup_sign_in_page(self):
        page = SignInPage(self.driver)
        page.click_sign_in_btn()  # going to sign_in_page
        return page
    def setup_otp_page(self):
        otp_page = VerifyOtpPage(self.driver)
        return otp_page

    def test_valid_sign_in(self):
        sign_in_page = self.setup_sign_in_page()
        sign_in_page.send_mobile_number(SignInData.valid_mobile_number)  # going to sign_in_page
        sign_in_page.check_box_check()  # going to sign_in_page
        sign_in_page.click_get_otp_btn() # going to sign_in_page
        sign_in_page.send_otp(SignInData.static_otp) # going to sign_in_page
        actual_title = sign_in_page.title() # coming from base_page
        expected_title = "Safe & Secure Mobile Recharges & Bill Payment"
        assert actual_title == expected_title,f"Expected title '{expected_title}', but found '{actual_title}'."
 

    # Positive cases
    # 🔽 NEW: one parametrized test for multiple test cases (TC_001 and TC_003)
    @pytest.mark.parametrize("tc_id,description,mobile_number,should_enable_otp",
                             signin_mobile_field__positive_cases,
                             ids =[item[0] for item in signin_mobile_field__positive_cases])
    def test_mobile_number_field_positive_validation(self,tc_id,description,mobile_number,should_enable_otp):
        sign_in_page = self.setup_sign_in_page()
        sign_in_page.send_mobile_number(mobile_number)
        sign_in_page.check_box_check()

        if tc_id == "TC_001":
            sign_in_page.click_get_otp_btn()
            actual_heading = self.setup_otp_page().get_page_heading()
            expected_heading = "Verify OTP"
            assert actual_heading == expected_heading, f"Expected '{expected_heading}', but got '{actual_heading}'"
        else:
            is_enabled = sign_in_page.is_enabled(sign_in_page.get_otp_btn)
            assert is_enabled,f"{tc_id} - {description}: Get OTP button should be enabled"



    # Negative cases
    # 🔽 NEW: one parametrized test for multiple test cases (TC_004–TC_009)
    @pytest.mark.parametrize("tc_id, description, mobile_number, shouldnot_enable_otp",
                             signin_mobile_field__negative_cases,
                             ids=[item[0] for item in signin_mobile_field__negative_cases] )
    def test_mobile_number_field_negative_validation(self, tc_id, description, mobile_number, shouldnot_enable_otp):
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
        if shouldnot_enable_otp is not None:
            is_enabled = sign_in_page.is_enabled(sign_in_page.get_otp_btn)

            if shouldnot_enable_otp:
                assert is_enabled, f"{tc_id} - {description}: Get OTP button should be ENABLED"
            else:
                assert not is_enabled, f"{tc_id} - {description}: Get OTP button should be DISABLED"


    
    # # TC_010 and TC_011
    # @pytest.mark.parametrize("tc_id, description, start_selected, expected_selected",terms_checkbox_cases,ids=[item[0] for item in terms_checkbox_cases],)
    # def test_terms_checkbox_behaviour(self, tc_id, description, start_selected, expected_selected):
    #     sign_in_page = self.setup_sign_in_page()

    #     sign_in_page.send_mobile_number(SignInData.valid_mobile_number)

    #     # Put checkbox in required initial state
    #     current = sign_in_page.is_selected(sign_in_page.check_box)
    #     if current != start_selected:
    #         sign_in_page.click(sign_in_page.check_box)
        
    #     current = sign_in_page.is_selected(sign_in_page.check_box)
    #     if current == start_selected:
    #         sign_in_page.click(sign_in_page.check_box)
    #         current = sign_in_page.is_selected(sign_in_page.check_box)
    #         if tc_id == "TC_010":
    #             assert current == expected_selected,f"{tc_id}:checkbox accepts check in unchecked state but it is {current}"
    #         else:
    #             assert current == expected_selected,f"{tc_id}:checkbox accepts uncheck in checked state but it is {current}"

    # TC_010 and TC_011
    @pytest.mark.parametrize(
    "tc_id, description, start_selected, expected_selected",
    terms_checkbox_cases,
    ids=[item[0] for item in terms_checkbox_cases],
    )
    def test_terms_checkbox_behaviour(self, tc_id, description, start_selected, expected_selected):
        sign_in_page = self.setup_sign_in_page()

        # PRECONDITION: a valid mobile so checkbox becomes enabled/clickable
        sign_in_page.send_mobile_number(SignInData.valid_mobile_number)

        # Ensure starting state (read from the hidden input)
        current = sign_in_page.is_terms_checkbox_selected()
        if current != start_selected:
            sign_in_page.click_terms_checkbox()
            # wait a short moment for state change
            sign_in_page.wait().until(lambda d: d.find_element(*sign_in_page.terms_checkbox_input).is_selected() == start_selected)

        # sanity check initial state
        assert sign_in_page.is_terms_checkbox_selected() == start_selected, f"{tc_id}: could not set initial state"

        # ACTION: toggle once (click visible switch)
        sign_in_page.click_terms_checkbox()

        # WAIT for expected final state
        sign_in_page.wait().until(lambda d: d.find_element(*sign_in_page.terms_checkbox_input).is_selected() == expected_selected)

        final_state = sign_in_page.is_terms_checkbox_selected()
        assert final_state == expected_selected, f"{tc_id}: {description} but checkbox state is {final_state}"



    # TC_012
    # from selenium.webdriver.support.ui import WebDriverWait
    # from selenium.webdriver.support import expected_conditions as EC

    # @pytest.mark.parametrize("tc_id, description, expected_url",terms_link_cases,ids=[item[0] for item in terms_link_cases],)
    # def test_terms_link_redirects_to_terms_page(self, tc_id, description, expected_url):
    #     sign_in_page = self.setup_sign_in_page()

    #     sign_in_page.click(sign_in_page.terms_link)

    #     WebDriverWait(self.driver, 10).until(
    #         EC.url_contains("/terms-condition")
    #     )

    #     current_url = self.driver.current_url
    #     assert expected_url in current_url, \
    #         f"{tc_id}: expected '{expected_url}', got '{current_url}'"


    #TC_13
    # @pytest.mark.parametrize(
    # "tc_id, description, tnc_checked",
    # terms_get_otp_cases,
    # ids=[item[0] for item in terms_get_otp_cases],
    # )
    # def test_get_otp_disabled_when_tnc_unchecked(self, tc_id, description, tnc_checked):
    #     sign_in_page = self.setup_sign_in_page()

    #     # Ensure checkbox is unchecked (for TC_013, tnc_checked = False)
    #     current = sign_in_page.is_selected(sign_in_page.check_box)
    #     if current != tnc_checked:
    #         sign_in_page.click(sign_in_page.check_box)

    #     assert sign_in_page.is_selected(sign_in_page.check_box) == tnc_checked

    #     # Now Get OTP must be disabled
    #     is_enabled = sign_in_page.is_enabled(sign_in_page.get_otp_btn)
    #     assert not is_enabled, \
    #         f"{tc_id}: Get OTP button should be DISABLED when T&C is unchecked"

