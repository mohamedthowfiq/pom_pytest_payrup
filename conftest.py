import pytest
from selenium import webdriver
from utilities.test_data import URLs
from selenium.webdriver.chrome.options import Options


# @pytest.fixture(params=["chrome","firefox","edge"])
@pytest.fixture(params=["chrome"])
def initialize_driver(request):
  if request.param == "chrome":
      # options = Options()

      # options.add_argument("--headless=new")
      # options.add_argument("--no-sandbox")
      # options.add_argument("--disable-dev-shm-usage")
      # options.add_argument("--window-size=1920,1080")

      # driver = webdriver.Chrome(options=options)
    driver = webdriver.Chrome()
  # elif request.param == "firefox":
  #   driver = webdriver.Firefox()
  # elif request.param == "edge":
  #   driver = webdriver.Edge()
  request.cls.driver = driver  # connects driver to class
  print("Browser: ",request.param) 
  driver.get(URLs.payrup)
  driver.maximize_window()

  yield
  print("Close driver")
  driver.quit() 


import os
from datetime import datetime

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # Only after test execution
    if report.when == "call": 
        driver = getattr(item.cls, "driver", None)
        if driver is None:
            return

        # Create folders
        base_dir = "screenshots"
        status_dir = "passed" if report.passed else "failed"
        save_dir = os.path.join(base_dir, status_dir)
        os.makedirs(save_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = item.name

        file_path = os.path.join(
            save_dir, f"{test_name}_{timestamp}.png"
        )

        driver.save_screenshot(file_path)
        print(f"\n📸 Screenshot saved: {file_path}")


