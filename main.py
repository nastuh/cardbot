from time import sleep
from selenium import webdriver
from selenium.common.expections import InvalidArgumentException

driver = webdriver.Chrome()
urls = [
    'https://www.google.com/',
    'https://www.youtube.com/',
    '',
    23,
    'https://algoritmika.org/ru',
    'ftp://algoritmika.org/ru',
]

for url in urls:
    try:
        driver.get(url)
    # Важно делать паузу между запросами
    except InvalidArgumentException:
        print(f'Данный url:{url} ломает нашу программу, мы его пропускаем')
    finally:
        sleep(3)