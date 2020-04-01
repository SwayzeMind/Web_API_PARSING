from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
import json
from pprint import pprint
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
mongodb = client['mail']
collection = mongodb['mail']

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://mail.ru')

elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'mailbox:login')))
elem.clear()
elem.send_keys('study.ai_172')
elem.send_keys(Keys.RETURN)
elem = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'mailbox:password')))
elem.send_keys('NewPassword172')
elem.send_keys(Keys.RETURN)

letters = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'js-letter-list-item')))

links = []
for i in letters:
    href = i.get_attribute('href')
    links.append(href)  # the driver.get link is broken

letters_list = []
for letter in links:
    the_list = {}
    driver.get(letter)  # driver.get link repaired
    subject = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'thread__subject'))).text
    date = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'letter__date'))).text
    sender = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'letter-contact'))).get_attribute('title')
    body = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'letter-body__body-content'))).text
    link = str(letter)
    collection.insert_one({'subject': subject, 'date': date, 'sender': sender, 'body': body, 'link':link})

    the_list['subject'] = subject
    the_list['date'] = date
    the_list['sender'] = sender
    the_list['body'] = body
    the_list['link'] = link
    letters_list.append(the_list)

pprint(letters_list)
#collection.insert_one(letters_list)   почему не работает вот так?

driver.quit()
