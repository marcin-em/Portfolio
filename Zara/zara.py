from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import time
import pyttsx3

# szukany kolor oraz rozmiar
COLOR = ''                      # np. 'Czarny' i 'M' - musi byc zachowany format jak na stronie 
SIZE = ''                       # (moze byc np. 'Czarny' lub 'CZARNY')
# interwal odswiezania strony
RELOAD_TIME = 5

EMAIL = ''
PASS = ''

# strona z szukanym produktem
URL = 'https://www.zara.com/pl/'
LOGIN_URL = 'https://www.zara.com/pl/pl/logon'
# sciezka do chromedriver.exe
PATH = "C:\\Program Files\\chromedriver.exe"

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(PATH, chrome_options=chrome_options)

engine = pyttsx3.init()

driver.get(LOGIN_URL)
driver.implicitly_wait(5)
cookies = driver.find_element_by_id('onetrust-accept-btn-handler')
time.sleep(1)
cookies.click()
username = driver.find_element_by_name('email')
password = driver.find_element_by_name('password')
username.send_keys(EMAIL)
password.send_keys(PASS)
login = driver.find_element_by_xpath('//*[@id="main"]/article/div/div/div[1]/section/form/div[2]/button/span')
ActionChains(driver).move_to_element(login).click().perform()

driver.get(URL)

product_found = False

def check_prod(btns):
    global product_found
    if btns == 1:
        jaki_kolor = driver.find_element_by_class_name('product-detail-info-color-selector__selected-color-name')
    else:
        jaki_kolor = driver.find_element_by_class_name('product-detail-info__color')
    if COLOR in jaki_kolor.text:
        # znalezienie listy z rozmiarami
        rozmiary = driver.find_elements_by_class_name('product-size-info__name')
        for rozmiar in rozmiary:
            if rozmiar.text == SIZE:
                # sprawdza czy jest dostepny
                grand = rozmiar.find_element_by_xpath('../../..')
                if grand.get_attribute('class') == 'product-size-selector__size-list-item':
                    print(f'Rozmiar {SIZE} jest dostepny')
                    product_found = True
                    break
        
def reload():
    print('Produkt niedostepny')
    time.sleep(RELOAD_TIME)
    driver.refresh()

while product_found == False:

    color_btns = driver.find_elements_by_class_name('product-detail-info-color-selector__color-button')
    if len(color_btns) > 0:
        for btn in color_btns:
            btn.click()
            check_prod(1)
            if product_found:
                break
    else:
        check_prod(0)

    if product_found:
        break
    reload()

engine.say('Produkt jest dostępny')
engine.runAndWait()