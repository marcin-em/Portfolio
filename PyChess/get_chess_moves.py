"""

Do testow:

http://chessebook.com/world.php?lan=en&match=1


"""


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
import os


PATH = "C:\\Program Files\\chromedriver.exe"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--mute-audio")
driver = webdriver.Chrome(PATH, chrome_options=chrome_options)

my_dir = os.getcwd()

KEY = 'wsadwsad'
WEB_SIGNIN = 'http://chessebook.com/signin.php?lan=en'

driver.get(WEB_SIGNIN)
driver.implicitly_wait(5)
driver.find_element_by_name('username').send_keys(KEY)
driver.find_element_by_name('password').send_keys(KEY)
driver.find_element_by_xpath('/html/body/div/div[3]/div/div[2]/div/div/form/div/button').click()
driver.implicitly_wait(5)

times = 1
index = 1
while times < 20:
    URL = f'http://chessebook.com/world_reti.php?lan=en&pos_ID={times}&match=9'
    driver.get(URL)
    move_list = []
    ok_moves = True
    while True:
        try:
            element = driver.find_element_by_xpath(f'/html/body/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td[3]/table/tbody/tr/td/nobr[{index}]')
            move_list.append(element.text)
            index += 1
        except:
            print(f'no more moves ({times})')
            index = 1
            break

    if ok_moves:
        formatted_list = []
        for move in move_list:
            if '0-0' in move:
                if '0-0-0' in move:
                    formatted_list.append('0-0-0')
                else:
                    formatted_list.append('0-0')
            else:
                fmove = move.replace(' ', '').replace('x', '').replace('-', '').replace('+', '')
                formatted_list.append(fmove[-4:])
        for fmove in formatted_list:
            with open('your_file.txt', 'a', encoding="utf-8") as f:
                f.write(fmove + ' ')
                f.close()
        with open('your_file.txt', 'a', encoding="utf-8") as f:
                f.write('\n')
                f.close()
        times += 1