import html.parser
import re
import time

from bs4 import BeautifulSoup

URL = r'http://ct.wunderbar.name/tpstud.php?tn={student_code}&exam={exam_code}'
TAG_RE = re.compile(r'<[^>]+>')
QUESTIONS_COUNT = 50
TEST_KEY = "2249310631"


def remove_tags(text):
    return TAG_RE.sub('', str(text))


def export(page_source, current_qa_dict):
    soup = BeautifulSoup(page_source, 'html.parser')
    current_qa_dict[remove_tags(soup.find('td', {'align': 'center'})).rstrip()] = [
        remove_tags(text) for text in soup.find_all('label')]


def connect(student_code, exam_code):
