from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Firefox()
driver.get("https://passport.yandex.ru/auth")

email = input('Введите Я.email: ')
passw = input('Введите пароль: ')

# email = 'email@ya.ru'
# passw = 'pass'

elem = driver.find_element(by=By.CLASS_NAME, value='Textinput-Control')
elem.send_keys(email)
elem = driver.find_element(by=By.ID, value='passp:sign-in')
elem.send_keys(Keys.RETURN)
elem = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "passp-field-passwd"))
)
elem.send_keys(passw)
elem.send_keys(Keys.RETURN)
elem = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'PasspAuthForm'))
)
elem = driver.find_elements(by=By.CLASS_NAME, value='Button2-Text')[1]
assert elem.text == 'Не сейчас'
driver.close()