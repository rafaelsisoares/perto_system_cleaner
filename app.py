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
    browser.implicitly_wait(5)
    email_input = browser.find_element(by=By.ID, value="inputEmail3")
    password_input = browser.find_element(by=By.ID, value="inputPassword3")
    submit = browser.find_element(by=By.CLASS_NAME, value="btn")
    email_input.send_keys(email)
    password_input.send_keys(password)
    submit.click()
    browser.implicitly_wait(2)
    browser.get(f"{url}/#/contractsB2C/accredited")
    browser.implicitly_wait(3)
    credentials = browser.find_element(by=By.TAG_NAME, value="tbody")
    credentials_table = credentials.find_elements(by=By.TAG_NAME, value="tr")
    for credential in credentials_table:
        edit_btn = credential.find_element(by=By.CLASS_NAME, value="btn-primary")
        edit_btn.click()
        nav_button = browser.find_element(by=By.LINK_TEXT, value="PORTADORES")
        nav_button.click()
        select = browser.find_element(by=By.TAG_NAME, value="select")



open_browser_session()
