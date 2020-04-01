from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
import json


client = MongoClient('localhost', 27017)
mongodb = client.mvideo
collection = mongodb['products']


chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome( options=chrome_options)

driver.get('https://www.mvideo.ru/')


while True:
    elem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="gallery-content accessories-new "][1]//a[contains(@class,"sel-hits-button-next")]')))
    if 'disabled' in elem.get_attribute('class'):
        break
    else:
        elem.click()



elem = driver.find_element_by_xpath('//div[@class="gallery-content accessories-new "]')
items = elem.find_elements_by_class_name('gallery-list-item')

for item in items:
    item_data = json.loads(item.find_element_by_xpath('.//a[@data-product-info]').get_attribute('data-product-info'))   # without the dot u get the same list
    collection.insert_one({'productId' : item_data['productId'],
                           'productVendorName' : item_data['productVendorName'],
                           'productName' : item_data['productName'],
                           'productPriceLocal' : item_data['productPriceLocal']})
driver.quit()