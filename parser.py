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
TEST_KEY = "2249310631"


def remove_tags(text):
    return TAG_RE.sub('', str(text))


def export(page_source, current_qa_dict):
    soup = BeautifulSoup(page_source, 'html.parser')
    current_qa_dict[remove_tags(soup.find('td', {'align': 'center'})).rstrip()] = [
        remove_tags(text) for text in soup.find_all('label')]


def parsek(output_dict):

    driver = webdriver.Chrome(chrome_options=OPTS)

    driver.get(URL)

    elem = driver.find_element_by_name('exam')
    elem.send_keys(TEST_KEY)
    elem.send_keys(Keys.ENTER)
    driver.find_element_by_class_name('button').click()

    for i in range(QUESTIONS_COUNT):
        source = driver.page_source
        export(source, output_dict)
        driver.find_element_by_class_name('button').click()

    driver.quit()


questions = dict()
parsek(questions)

with open('questions.txt', 'a') as file:
    file.write(str(questions))
