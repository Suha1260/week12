
import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


BASE_URL = "http://127.0.0.1:5000/"


@pytest.fixture
def setup_teardown():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    yield driver

    driver.quit()


def get_alert_text(driver):
    alert = WebDriverWait(driver, 5).until(
        lambda d: d.switch_to.alert
    )
    message = alert.text
    Alert(driver).accept()
    return message


def test_empty_username(setup_teardown):
    driver = setup_teardown
    driver.get(BASE_URL)

    driver.find_element(By.NAME, "username").clear()
    driver.find_element(By.NAME, "pwd").send_keys("Password123")
    driver.find_element(By.NAME, "sb").click()

    assert get_alert_text(driver) == "Username cannot be empty."


def test_empty_password(setup_teardown):
    driver = setup_teardown
    driver.get(BASE_URL)

    driver.find_element(By.NAME, "username").send_keys("John")
    driver.find_element(By.NAME, "pwd").clear()
    driver.find_element(By.NAME, "sb").click()

    assert get_alert_text(driver) == "Password cannot be empty."


def test_short_password(setup_teardown):
    driver = setup_teardown
    driver.get(BASE_URL)

    driver.find_element(By.NAME, "username").send_keys("Jane")
    driver.find_element(By.NAME, "pwd").send_keys("abc1")
    driver.find_element(By.NAME, "sb").click()

    assert get_alert_text(driver) == (
        "Password must be at least 6 characters long."
    )


def test_valid_input(setup_teardown):
    driver = setup_teardown
    driver.get(BASE_URL)

    driver.find_element(By.NAME, "username").send_keys("Suha")
    driver.find_element(By.NAME, "pwd").send_keys("Password123")
    driver.find_element(By.NAME, "sb").click()

    WebDriverWait(driver, 5).until(
        lambda d: "/submit" in d.current_url
    )

    assert "Hello, Suha! Welcome to the website" in driver.page_source

