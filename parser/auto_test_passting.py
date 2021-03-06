import html.parser
import re
import time
import requests

from bs4 import BeautifulSoup

URL = r'http://ct.wunderbar.name/tpstud.php?tn={student_code}&exam={exam_code}'
TAG_RE = re.compile(r'<[^>]+>')
QUESTIONS_COUNT = 50
TEST_KEY = "2249310631"

driver = webdriver.Chrome(r"C:\Users\Nik\Desktop\chromedriver.exe")
driver.get(URL.format('512'))
elem = driver.find_element_by_name('exam')
elem.send_keys("2507813895")
elem.send_keys(Keys.ENTER)
driver.find_element_by_class_name('button').click()

for question in range(QUESTIONS_COUNT):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    question = get_question(soup)
    if question in qdict:
        answers = [answer for answer in qdict[question].keys(
        ) if qdict[question][answer]['сorrectness'] == True]
        if answers != []:
            if 'value' in answers[0]:
                css_selector_string = 'input[name="{0}"]'
            else:
                css_selector_string = 'input[value="{0}"]'
            for answer in answers:
                driver.find_element_by_css_selector(
                    css_selector_string.format(answer)).click()
            # time.sleep(5)
    driver.find_element_by_name('go').click()
time.sleep(50)
driver.quit()
