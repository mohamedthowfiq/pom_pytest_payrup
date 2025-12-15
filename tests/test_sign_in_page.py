from tests.base_test import BaseTest
from pages.sign_in_page import SignInPage
from utilities.test_data import SignInData,\
                    signin_mobile_field__negative_cases,\
                    signin_mobile_field__positive_cases,\
                    terms_checkbox_cases,\
                    terms_link_cases,\
                    terms_get_otp_cases,\
                    verify_otp_positive_cases,\
                    verify_otp_negative_cases
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
import pytest
import time


class TestSignInPage(BaseTest):

    def setup_sign_in_page(self):
        page = SignInPage(self.driver)
        page.click_sign_in_btn()  # going to sign_in_page
        return page

    # def test_valid_sign_in(self):
    #     sign_in_page = self.setup_sign_in_page()
    #     sign_in_page.send_mobile_number(SignInData.valid_mobile_number)  # going to sign_in_page
    #     sign_in_page.check_box_check()  # going to sign_in_page
    #     sign_in_page.click_get_otp_btn() # going to sign_in_page
    #     sign_in_page.send_otp(SignInData.static_otp) # going to sign_in_page
    #     actual_title = sign_in_page.title() # coming from base_page
    #     expected_title = "Safe & Secure Mobile Recharges & Bill Payment"
    #     assert actual_title == expected_title,f"Expected title '{expected_title}', but found '{actual_title}'."
 

    # Positive cases
    # 🔽 NEW: one parametrized test for multiple test cases (TC_001 and TC_002)
    @pytest.mark.parametrize(
    "tc_id,description,mobile_number,should_enable_otp",
    signin_mobile_field__positive_cases,
    ids=[item[0] for item in signin_mobile_field__positive_cases])
    def test_mobile_number_field_positive_validation(self, tc_id, description, mobile_number, should_enable_otp):
        sign_in_page = self.setup_sign_in_page()
        sign_in_page._step_counter = 1

        sign_in_page.send_mobile_number(mobile_number)
        sign_in_page.step(tc_id, "mobile_number_entered")

        sign_in_page.check_box_check()
        sign_in_page.step(tc_id, "terms_checked")

        if tc_id == "TC_001":
            sign_in_page.click_get_otp_btn()
            sign_in_page.step(tc_id, "get_otp_clicked")

            actual_heading = sign_in_page.get_otp_box_heading()
            sign_in_page.step(tc_id, "verify_otp_page_displayed")

            assert actual_heading == "Verify OTP", (
                f"Expected 'Verify OTP', but got '{actual_heading}'"
            )
        else:
            is_enabled = sign_in_page.is_enabled(sign_in_page.get_otp_btn)
            sign_in_page.step(tc_id, "get_otp_button_enabled")

            assert is_enabled, (
                f"{tc_id} - {description}: Get OTP button should be enabled"
            )




    # Negative cases
    # 🔽 NEW: one parametrized test for multiple test cases (TC_003–TC_008)
    @pytest.mark.parametrize("tc_id, description, mobile_number, shouldnot_enable_otp",
                             signin_mobile_field__negative_cases,
                             ids=[item[0] for item in signin_mobile_field__negative_cases] )
    def test_mobile_number_field_negative_validation(self, tc_id, description, mobile_number, shouldnot_enable_otp):
        sign_in_page = self.setup_sign_in_page()
        sign_in_page.send_mobile_number(mobile_number)
        sign_in_page.check_box_check()

         # 🔹 Special validation for TC_004: field must not accept > 10 digits
        if tc_id == "TC_004":
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


    # TC_009 and TC_010
    @pytest.mark.parametrize("tc_id, description, start_selected, expected_selected",terms_checkbox_cases,
                              ids=[item[0] for item in terms_checkbox_cases],)
    def test_terms_checkbox_behaviour(self, tc_id, description, start_selected, expected_selected):
        sign_in_page = self.setup_sign_in_page()

        # PRECONDITION: a valid mobile so checkbox becomes enabled/clickable
        sign_in_page.send_mobile_number(SignInData.valid_mobile_number)

        # Ensure starting state
        sign_in_page.ensure_state(
                sign_in_page.terms_checkbox_click,
                sign_in_page.terms_checkbox_input,
                start_selected
            )
        
        # toggle action
        sign_in_page.click_terms_checkbox()

        # WAIT final state
        sign_in_page.wait_for_condition(lambda d:sign_in_page.is_terms_checkbox_selected() == expected_selected)

        assert sign_in_page.is_terms_checkbox_selected() == expected_selected, f"{tc_id}: {description} but checkbox state is {sign_in_page.is_terms_checkbox_selected()}"



    # TC_011
    @pytest.mark.parametrize("tc_id, description, expected_url",terms_link_cases,ids=[item[0] for item in terms_link_cases],)
    def test_terms_link_redirects_to_terms_page(self, tc_id, description, expected_url):
        sign_in_page = self.setup_sign_in_page()
        parent_1 = sign_in_page.current_window_handle()
        sign_in_page.click_terms_n_conditions_link()
        # Wait for the new tab
        sign_in_page.wait().until( lambda d: len(d.window_handles) > 1)
        # Get the new tab handle
        new_handle = [h for h in sign_in_page.driver.window_handles if h != parent_1][0]
        # Switch to the new tab
        sign_in_page.driver.switch_to.window(new_handle)
        actual_url = sign_in_page.current_url()
        assert expected_url in actual_url,f"{tc_id}: expected '{expected_url}', got '{actual_url}'"


    # TC_012
    @pytest.mark.parametrize("tc_id, description, tnc_checked",terms_get_otp_cases,ids=[item[0] for item in terms_get_otp_cases],)
    def test_get_otp_disabled_when_tnc_unchecked(self, tc_id, description, tnc_checked):
        sign_in_page = self.setup_sign_in_page()

        # Ensure checkbox is unchecked (for TC_013, tnc_checked = False)
        current = sign_in_page.is_terms_checkbox_selected()

        if current != tnc_checked:
            sign_in_page.click(sign_in_page.terms_checkbox_click)

        assert sign_in_page.is_selected(sign_in_page.terms_checkbox_input) == tnc_checked

        # Now Get OTP must be disabled
        is_enabled = sign_in_page.is_enabled(sign_in_page.get_otp_btn)
        assert not is_enabled,f"{tc_id}: Get OTP button should be DISABLED when T&C is unchecked"


    # valid otp box  TC_013-TC_015
    @pytest.mark.parametrize("tc_id, description, value",verify_otp_positive_cases,ids=[item[0] for item in verify_otp_positive_cases])
    def test_verify_otp_box_positive_validation(self, tc_id, description, value):
        sign_in_page = self.setup_sign_in_page()

        sign_in_page.send_mobile_number(SignInData.valid_mobile_number)
        sign_in_page.check_box_check()
        sign_in_page.click_get_otp_btn()
        assert sign_in_page.get_otp_box_heading()=='Verify OTP', f"{tc_id}: OTP box did not appear."

        # TC_013 → no OTP input, just check box presence
        if tc_id == "TC_013":
            sign_in_page.click(sign_in_page.edit_icon)
            assert sign_in_page.get_signin_box_heading() == 'Sign in to payRup',f"{tc_id}:failed to redirect to sign in to payRup box"

        # TC_014 → numeric OTP → Verify button should be ENABLED (but invalid)
        if tc_id == "TC_014":
            sign_in_page.click(sign_in_page.otp_field)
            sign_in_page.send_keys(sign_in_page.otp_field,value)
            field_value = sign_in_page.get_attribute(sign_in_page.otp_field,"value")
            assert field_value == value,f"{tc_id}:input field doesn't accept number as input"

        # TC_015 needs static OTP even though placeholder exists
        if tc_id == "TC_015":
            sign_in_page.click(sign_in_page.otp_field)
            sign_in_page.send_keys(sign_in_page.otp_field,SignInData.static_otp)
            assert sign_in_page.title() == "Safe & Secure Mobile Recharges & Bill Payment",f"{tc_id}:some thing didn't went well"


    # valid otp box  TC_016-TC_025
    @pytest.mark.parametrize("tc_id, description, value",verify_otp_negative_cases,ids=[item[0] for item in verify_otp_negative_cases])
    def test_verify_otp_box_negative_validation(self, tc_id, description, value):
        sign_in_page = self.setup_sign_in_page()

        sign_in_page.send_mobile_number(SignInData.valid_mobile_number)
        sign_in_page.check_box_check()
        sign_in_page.click_get_otp_btn()
        assert sign_in_page.get_otp_box_heading()=='Verify OTP', f"{tc_id}: OTP box did not appear."

        # In all these: Verify button should be disabled
        # TC_016, TC_017, TC_018, TC_020, TC_021
        if tc_id in ["TC_016","TC_017","TC_018"]:
            sign_in_page.send_keys(sign_in_page.otp_field,value)   # alphabets # special char
            otp_value = sign_in_page.get_attribute(sign_in_page.otp_field, "value")
            if tc_id == "TC_018":
                assert " " not in otp_value, f"{description}, but value was: " + otp_value
                return
            if tc_id in ["TC_016","TC_017"]:
                assert otp_value == "", f"{description}, but value was: " + otp_value
                return
                
        # TC_019 → Blank OTP → Verify button must be disabled
        if tc_id == "TC_019":
            assert not sign_in_page.is_enabled(sign_in_page.verify_btn), f"{tc_id}: Verify button should be disabled for blank OTP"
            return
        if tc_id == "TC_020":
            sign_in_page.click(sign_in_page.otp_field)
            sign_in_page.send_keys(sign_in_page.otp_field,value)
            assert not sign_in_page.is_enabled(sign_in_page.verify_btn), f"{tc_id}: Verify button should be disabled for blank OTP"
            return
        
          # 🔹 Special validation for TC_021: field must not accept 5 digits
        if tc_id == "TC_021":
            sign_in_page.send_keys(sign_in_page.otp_field,value)
            entered_value = sign_in_page.get_entered_otp_number()
            assert len(entered_value) == 4, f"{tc_id}: field should only contain 4 digits"
            assert entered_value == value[:4], (
                f"{tc_id}: field should keep only first 4 digits; "
                f"expected '{value[:10]}', got '{entered_value}'"
            )

        if tc_id == "TC_022":
            sign_in_page.send_keys(sign_in_page.otp_field,value)
            assert sign_in_page.display_warning_msg("Invalid OTP!") == "Invalid OTP!",f"{tc_id}:Warning sms not found"
            assert sign_in_page.is_enabled(sign_in_page.verify_btn),f"{tc_id}: Verify button should be disabled for invalid OTP"
            return
        
       


        def timer_to_seconds(text: str) -> int:
            try:
                m, s = text.strip().split(":")
                return int(m) * 60 + int(s)
            except Exception:
                return -1

        if tc_id == "TC_023":
            # read the timer text (e.g. "00:56")
            timer_text_before = sign_in_page.text(sign_in_page.countdown_timer).strip()
            secs_before = timer_to_seconds(timer_text_before)
            assert secs_before > 0, f"{tc_id}: Expected timer > 0, got '{timer_text_before}'"

            # find resend element and try to click it
            resend_el = sign_in_page.find(sign_in_page.resend_otp)

            try:
                resend_el.click()
            except WebDriverException:
                # sometimes click may be blocked by overlay; that's acceptable for this test
                pass

            # short wait for UI reaction (if any)
            time.sleep(1.2)

            # read timer again
            timer_text_after = sign_in_page.text(sign_in_page.countdown_timer).strip()
            secs_after = timer_to_seconds(timer_text_after)
            assert secs_after >= 0, f"{tc_id}: Could not parse timer after clicking. Found '{timer_text_after}'"

            # If clicking triggered a resend we'd expect the timer to reset upwards (e.g. to 59),
            # so secs_after should NOT be greater than secs_before. Accept equal or decreased value.
            assert secs_after <= secs_before, (
                f"{tc_id}: Clicking Resend while timer>0 should NOT reset timer. "
                f"Before={timer_text_before}, After={timer_text_after}"
            )

            # Verify button remains disabled
            assert not sign_in_page.is_enabled(sign_in_page.verify_btn), f"{tc_id}: Verify button should remain disabled while timer running"
            return
        


        def timer_to_seconds(text: str) -> int:
            try:
                m, s = text.strip().split(":")
                return int(m) * 60 + int(s)
            except Exception:
                return -1

        if tc_id == "TC_024":
            driver = sign_in_page.driver

            # 1️⃣ Wait until timer becomes 00:00
            try:
                WebDriverWait(driver, 75, poll_frequency=0.5).until(
                    lambda d: sign_in_page.text(sign_in_page.countdown_timer).strip() == "00:00"
                )
            except TimeoutException:
                raise AssertionError(f"{tc_id}: Timer did not reach 00:00 within timeout.")

            assert sign_in_page.text(sign_in_page.countdown_timer).strip() == "00:00", \
                f"{tc_id}: Timer expected 00:00"

            # 2️⃣ Click Resend OTP
            try:
                if hasattr(sign_in_page, "safe_click"):
                    sign_in_page.safe_click(sign_in_page.resend_otp, timeout=5)
                else:
                    sign_in_page.click(sign_in_page.resend_otp)
            except WebDriverException:
                el = sign_in_page.find(sign_in_page.resend_otp, timeout=3)
                driver.execute_script("arguments[0].click();", el)

            # 3️⃣ Wait for UI update and validate timer reset
            time.sleep(1.2)

            timer_after = sign_in_page.text(sign_in_page.countdown_timer).strip()
            secs_after = timer_to_seconds(timer_after)
            assert secs_after > 0, \
                f"{tc_id}: After resend, timer should reset (>0), but found '{timer_after}'"

            # 🔴 🔴 🔴 PLACE MESSAGE VALIDATION RIGHT HERE 🔴 🔴 🔴
            msg = sign_in_page.get_visible_otp_message()
            assert msg == "OTP sent to your number successfully.", \
                f"{tc_id}: Expected OTP success message, but got '{msg}'"

            # 4️⃣ Final guard: Verify button state
            assert not sign_in_page.is_enabled(sign_in_page.verify_btn), \
                f"{tc_id}: Verify button expected to be disabled after resend"

            return
        
        # if tc_id == "TC_025":
        #     invalid_otp = value
        #     lock_msg = "please try again after 1 hour"

        #     # Enter OTP once
        #     sign_in_page.send_keys(sign_in_page.otp_field, invalid_otp)

        #     max_attempts = 10
        #     msg = None

        #     for _ in range(max_attempts):
        #         # RAPID click (no sleep)
        #         try:
        #             sign_in_page.click(sign_in_page.verify_btn)
        #         except Exception:
        #             pass

        #         msg = sign_in_page.get_visible_otp_message()

        #         if msg == lock_msg:
        #             break

        #     assert msg == lock_msg, \
        #         f"{tc_id}: Expected lock message '{lock_msg}', but got '{msg}'"

        #     return



        


