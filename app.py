from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
from time import sleep
import os


def open_browser_session() -> None:
    load_dotenv()
    url = os.getenv("URL")
    email = os.getenv("EMAIL")
    password = os.getenv("PASS")
    browser = webdriver.Chrome()
    hold = WebDriverWait(browser, timeout=10)
    browser.get(url)
    hold.until(EC.visibility_of_element_located((By.ID, "inputEmail3")))
    email_input = browser.find_element(by=By.ID, value="inputEmail3")
    password_input = browser.find_element(by=By.ID, value="inputPassword3")
    submit = browser.find_element(by=By.CLASS_NAME, value="btn")
    email_input.send_keys(email)
    password_input.send_keys(password)
    submit.click()
    aside_menu = hold.until(EC.visibility_of_element_located((By.TAG_NAME, "aside")))
    sub_menu = aside_menu.find_element(by=By.LINK_TEXT, value="Contr. Credenciados")
    sub_menu.click()
    credentials_ctrl = browser.find_element(by=By.LINK_TEXT, value="Credenciado")
    credentials_ctrl.click()
    credentials = browser.find_element(by=By.TAG_NAME, value="tbody")
    credentials_table = credentials.find_elements(by=By.TAG_NAME, value="tr")
    sleep(2)
    for credential in credentials_table:
        edit_btn = credential.find_element(by=By.CLASS_NAME, value="btn-primary")
        edit_btn.click()
        nav_button = browser.find_element(by=By.LINK_TEXT, value="PORTADORES")
        nav_button.click()
        select_menu = hold.until(EC.element_to_be_clickable(
            (By.NAME, "inputSignatures")))
        select = Select(select_menu)
        options = [
            o.get_attribute("textContent").strip() for o in select.options]
        print(options)
        select.select_by_visible_text(options[1])
        users_table = hold.until(
            EC.visibility_of_element_located((By.TAG_NAME, "tbody")))


open_browser_session()
