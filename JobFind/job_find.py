from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def zatwierdz():
    zatwierdz = driver.find_element_by_xpath("//*[contains(text(), ' Zatwierdź ')]")
    driver.execute_script("arguments[0].click();", zatwierdz)   

NFJ = 'https://nofluffjobs.com/pl'
BDJ = 'https://bulldogjob.pl/companies/jobs'
INFO = 'https://www.infopraca.pl/praca?q=junior&ct=it-programowanie-analizy&d=0&lc=Warszawa'
PATH = "C:\\Program Files\\chromedriver.exe"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("prefs", {"profile.default_content_settings.cookies": 2})
chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications" : 2})
capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "eager"
driver = webdriver.Chrome(PATH, chrome_options=chrome_options, desired_capabilities=capa)

# NoFluffJobs
driver.get(NFJ)
driver.implicitly_wait(5)
driver.find_element_by_xpath("//*[contains(text(), ' Wyrażam zgodę ')]").click()

# Lokalizacja
driver.find_element_by_xpath("//*[contains(text(), 'Lokalizacje')]").click()
driver.find_element_by_xpath("//*[contains(text(), 'Warszawa')]").click()
zatwierdz()

# Filtry
driver.find_element_by_xpath("//*[contains(text(), 'Filtry')]").click()
stazysta = driver.find_element_by_xpath("//*[contains(text(), ' Stażysta ')]")
junior = driver.find_element_by_xpath("//*[contains(text(), ' Junior ')]")
driver.execute_script("arguments[0].click();", stazysta) 
driver.execute_script("arguments[0].click();", junior) 
zatwierdz()

# BulldogJob
driver.execute_script(f"window.open('{BDJ}');")
driver.switch_to.window(driver.window_handles[-1])
wawa = driver.find_element_by_id('city_warszawa')
junior = driver.find_element_by_id('exp_level_junior')
driver.execute_script("arguments[0].click();", wawa)
driver.execute_script("arguments[0].click();", junior)

# InfoPraca
driver.execute_script(f"window.open('{INFO}');")
driver.switch_to.window(driver.window_handles[-1])

driver.maximize_window()

print('Good luck! ;)')