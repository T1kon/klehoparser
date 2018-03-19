import html.parser
import re
import time

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

URL = r'http://ct.wunderbar.name/tpstud.php?tn=512'
TAG_RE = re.compile(r'<[^>]+>')
QUESTIONS_COUNT = 50
OPTS = webdriver.ChromeOptions()
OPTS.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"


def remove_tags(text):
    return TAG_RE.sub('', str(text))


def parsek(output_dict):

    driver = webdriver.Chrome(chrome_options=OPTS)

    driver.get(URL)
    # time.sleep(0.01)

    elem = driver.find_element_by_name('exam')
    elem.send_keys("521703471")
    elem.send_keys(Keys.ENTER)
    # time.sleep(0.01)

    driver.find_element_by_class_name('button').click()
    # time.sleep(0.01)

    for i in range(QUESTIONS_COUNT):
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        output_dict[remove_tags(soup.find('td', {'align': 'center'})).rstrip()] = [
            remove_tags(text) for text in soup.find_all('label')]
        # time.sleep(0.01)
        driver.find_element_by_class_name('button').click()
    driver.quit()


questions = dict()
parsek(questions)

with open('asd.txt', 'a') as file:
    file.write(str(questions))
