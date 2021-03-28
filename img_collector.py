import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import openpyxl
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

filepath = input('xlsx 파일명을 입력해주세요 ex) test.xlsx > ')
url = input('구글이미지 URL을 입력해주세요 > ')
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument('window-size=1920x1080')
options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get(url)


SCROLL_PAUSE_TIME = 2

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(SCROLL_PAUSE_TIME)

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        try:
            driver.find_element_by_css_selector('.mye4qd').click()
        except:
            break
    last_height = new_height

# == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =

images = driver.find_elements_by_css_selector('.rg_i.Q4LuWd')[:]

wb = openpyxl.Workbook()
ws = wb.active


for image in images:
    try:
        image.click()
        time.sleep(5)

        img_url = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id = "Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div/div[2]/a/img'))).get_attribute("src")

        if 'data:image' in img_url:
            print('패스합니다 data')
        else:
            ws.append([img_url])
            wb.save(filepath)
            print('저장이 완료되었습니다.')

    except:
        pass

driver.close()
wb.close()
print('끗!')
