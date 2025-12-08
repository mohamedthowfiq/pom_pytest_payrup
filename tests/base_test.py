import pytest


@pytest.mark.usefixtures("initialize_driver")  # coming from confest.py
class BaseTest:
    pass