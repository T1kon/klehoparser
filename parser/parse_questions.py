import html.parser
import json
import re
import time
import random
from os.path import getsize, isfile

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

URL = r'http://ct.wunderbar.name/tpstud.php?tn={0}'
TAG_RE = re.compile(r'<[^>]+>')
QUESTIONS_COUNT = 50
OPTS = webdriver.ChromeOptions()


def remove_tags(text):
    return TAG_RE.sub('', str(text))


def export(page_source, current_qa_dict):
    soup = BeautifulSoup(page_source, 'html.parser')
    key = get_question(soup)
    if soup.find_all("input", {"name": "radio1"}) != []:
        current_qa_dict[key] = {strong_tag['value']: {'сorrectness': False, 'answer': " * " + strong_tag.next_sibling} for strong_tag in soup.find_all(
            "input", {"name": "radio1"})}
    else:
        current_qa_dict[key] = {strong_tag['name']: {'сorrectness': False, 'answer': " - " + strong_tag.next_sibling} for strong_tag in soup.find_all(
            "input", {"type": "checkbox"})}


def connect_to_test(student_code, exam_code):

    driver = webdriver.Chrome(r"chromedriver.exe")
    driver.get(URL.format(student_code))
    elem = driver.find_element_by_name('exam')
    elem.send_keys(exam_code)
    elem.send_keys(Keys.ENTER)

    driver.find_element_by_class_name('button').click()
    result = parsek(driver)
    driver.quit()

    return result


def get_question(soup):
    return remove_tags(soup.find('td', {'align': 'center'})).split("\n", 1)[0]


def parsek(driver):

    output_dict = {}

    for question in range(QUESTIONS_COUNT):
        source = driver.page_source
        export(source, output_dict)
        driver.find_element_by_name('go').click()
    return output_dict


def record_into_file(file_name, qdict):
    if getsize(file_name) > 0:
        with open(file_name, 'rt+') as file:
            file_dict = json.load(file)
            qdict.update(file_dict)

    with open(file_name, 'wt+') as file:
        json.dump(qdict, file, ensure_ascii=False)
        print(len(qdict))


def export_into_readable(import_name, export_name):
    with open(export_name, "rt+") as file:
        export_dict = json.load(file)

    with open(import_name, "wt+") as file:
        for key in export_dict:
            file.write(key)
            file.write("\n")
            for value in export_dict[key]:
                file.writelines(value)
                file.write("\n")
            file.write("\n")


#qdict = json.load(open("questions.json", "rt+"))

file_name = "questions.json"
#readable = "klehoparser/questions.txt"
for i in range(3):
    if isfile(file_name):
        record_into_file(file_name, connect_to_test('512', "2507813895"))
    else:
        print("File does not exist")
# export_into_readable(readable, file_name)
"""
driver = webdriver.Chrome(r"chromedriver.exe")
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
    driver.find_element_by_name('go').click()
time.sleep(50)
driver.quit()
"""
