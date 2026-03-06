from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
from time import sleep
import os


def open_browser_session() -> None:
    load_dotenv()
    browser_options = Options()
    browser_options.add_argument("start-maximized")
    browser_options.add_argument("--disable-notifications")
    url = os.getenv("URL")
    email = os.getenv("EMAIL")
    password = os.getenv("PASS")
    browser = webdriver.Chrome(options=browser_options)
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
    credentials = hold.until(EC.visibility_of_element_located((By.TAG_NAME, "tbody")))
    credentials_table = credentials.find_elements(by=By.TAG_NAME, value="tr")
    credentials_table.pop(1)
    sleep(2)
    for i in range(len(credentials_table)):
        credential = credentials_table[i]
        edit_btn = credential.find_element(by=By.CLASS_NAME, value="btn-primary")
        edit_btn.click()
        nav_button = browser.find_element(by=By.LINK_TEXT, value="PORTADORES")
        nav_button.click()
        select_menu = hold.until(EC.element_to_be_clickable(
            (By.NAME, "inputSignatures")))
        select = Select(select_menu)
        options = [
            o.get_attribute("textContent").strip() for o in select.options]
        select.select_by_visible_text(options[1])
        path = "//table[@id='exportable']//tbody//tr"
        hold.until(lambda d: len(d.find_elements(By.XPATH, path)) > 1)
        num_pages = browser.find_element(
            by=By.CLASS_NAME, value="select-page"
            ).get_attribute("max")
        for _ in range(int(num_pages)):
            users_table = browser.find_elements(by=By.XPATH, value=path)
            users_table.pop(0)
            for user in users_table:
                btn_container = user.find_elements(by=By.TAG_NAME, value="td")[-1]
                edit = btn_container.find_element(by=By.CLASS_NAME, value="btn-primary")
                browser.execute_script("arguments[0].click();", edit)
                pop_up = hold.until(EC.visibility_of_element_located((By.CLASS_NAME, "modal-content")))
                close = pop_up.find_element(by=By.CLASS_NAME, value="btn-warning")
                try:
                    registers_table = hold.until(EC.visibility_of_element_located((By.TAG_NAME, "tbody")))
                except TimeoutException:
                    print("Este usuario não possui registros")
                    browser.execute_script("arguments[0].click();", close)
                    continue
                registers = registers_table.find_elements(by=By.TAG_NAME, value="tr")
                if len(registers) > 0:
                    for register in registers:
                        data = register.find_elements(by=By.TAG_NAME, value="td")
                        if data[0].get_attribute("textContent") == "CÓDIGO DE BARRAS":
                            btn_remove = data[-1].find_element(by=By.CLASS_NAME, value="btn-danger")
                            btn_remove.click()
                            try:
                                registers_table = hold.until(EC.visibility_of_element_located((By.TAG_NAME, "tbody")))
                                registers = registers_table.find_elements(by=By.TAG_NAME, value="tr")
                            except TimeoutException:
                                continue
                        sleep(2)
                browser.execute_script("arguments[0].click();", close)
                hold.until(EC.invisibility_of_element_located(pop_up))
            if int(num_pages) > 1:
                next_page = browser.find_element(by=By.LINK_TEXT, value=">")
                next_page.click()
            #sleep(3)
        footer = browser.find_element(by=By.CLASS_NAME, value="panel-footer")
        btn_close = footer.find_element(by=By.TAG_NAME, value="button")
        btn_close.click()
        sleep(3)
        credentials = hold.until(EC.visibility_of_element_located((By.TAG_NAME, "tbody")))
        credentials_table = credentials.find_elements(by=By.TAG_NAME, value="tr")

if __name__ == "__main__":
    open_browser_session()
