# utilities/test_data.py
class URLs:
    payrup = "https://payrup.com/"
    terms_conditions = "https://payrup.com/terms-condition"


class SignInData:
    # common data
    # valid_mobile_number = "9066353121"
    static_otp = "9999"

    # field validation numbers
    invalid_mobile_number = "1234567890"
    valid_mobile_number = "9066353121"     # TC_002
    nine_digit_mobile = "123456789"        # TC_003
    eleven_digit_mobile = "12345678901"    # TC_004
    alphabet_mobile = "abcdefghij"         # TC_005
    specialchar_mobile = "@#$%"            # TC_006
    space_mobile = "  "                    # TC_007
    blank = ""                             # TC_008


signin_mobile_field__positive_cases = [
    ("TC_001", "redirects to Verify OTP box", SignInData.valid_mobile_number,   True),
    ("TC_002", "accept exactly 10 digits",    SignInData.valid_mobile_number,   True),
]

signin_mobile_field__negative_cases = [
    ("TC_003", "9 digit - invalid",               SignInData.nine_digit_mobile,          False),
    ("TC_004", "11 digits - invalid",             SignInData.eleven_digit_mobile,        None),
    ("TC_005", "alphabets not allowed",           SignInData.alphabet_mobile,            False),
    ("TC_006", "special characters not allowed",  SignInData.specialchar_mobile,         False),
    ("TC_007", "space not allowed",               SignInData.space_mobile,               False),
    ("TC_008", "blank not allowed",               SignInData.blank,                      False),
]

# ----------------- Terms & Conditions Test Cases -----------------

# TC_010 → checkbox accepts CHECK when unchecked
# TC_011 → checkbox accepts UNCHECK when checked
terms_checkbox_cases = [
    # tc_id,   description,                                   start_state, expected_state
    ("TC_009", "checkbox accepts check when unchecked",       False,       True),
    ("TC_010", "checkbox accepts uncheck when checked",       True,        False),
]

# TC_012 → clicking terms link redirects user to correct page
terms_link_cases = [
    ("TC_011", "terms link redirects to terms page", URLs.terms_conditions),
]

# TC_013 → Get OTP should be disabled when checkbox is unchecked
terms_get_otp_cases = [
    ("TC_012", "Get OTP disabled when T&C unchecked", False),
]
