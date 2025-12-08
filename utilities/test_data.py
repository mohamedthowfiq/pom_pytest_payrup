# utilities/test_data.py
class URLs:
    payrup = "https://payrup.com/"


class SignInData:
    # common data
    valid_mobile_number = "9066353121"
    static_otp = "9999"

    # field validation numbers
    invalid_mobile_number = "1234567890"
    valid_mobile_number = "9066353121"     # TC_003
    nine_digit_mobile = "123456789"        # TC_004
    eleven_digit_mobile = "12345678901"    # TC_005
    alphabet_mobile = "abcdefghij"         # TC_006
    specialchar_mobile = "@#$%"            # TC_007
    space_mobile = "  "                    # TC_008
    blank = ""                             # TC_009


signin_mobile_field__positive_cases = [
    # ("TC_002", "accept numbers",                    SignInData.valid_mobile_number,        True),
    ("TC_003", "accept exactly 10 digits",        SignInData.valid_mobile_number,        True),
]

signin_mobile_field__negative_cases = [
    ("TC_004", "9 digit - invalid",               SignInData.nine_digit_mobile,          False),
    ("TC_005", "11 digits - invalid",             SignInData.eleven_digit_mobile,        None),
    ("TC_006", "alphabets not allowed",           SignInData.alphabet_mobile,            False),
    ("TC_007", "special characters not allowed",  SignInData.specialchar_mobile,         False),
    ("TC_008", "space not allowed",               SignInData.space_mobile,               False),
    ("TC_009", "blank not allowed",               SignInData.blank,                      False),
]
