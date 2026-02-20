from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os


def open_browser_session() -> None:
    load_dotenv()
    url = os.getenv("URL")
    email = os.getenv("EMAIL")
    password = os.getenv("PASS")
    browser = webdriver.Chrome()
    browser.get(url)
    browser.implicitly_wait(1)
    email_input = browser.find_element(by=By.ID, value="inputEmail3")
    password_input = browser.find_element(by=By.ID, value="inputPassword3")
    submit = browser.find_element(by=By.CLASS_NAME, value="btn")
    email_input.send_keys(email)
    password_input.send_keys(password)
    submit.click()


open_browser_session()
