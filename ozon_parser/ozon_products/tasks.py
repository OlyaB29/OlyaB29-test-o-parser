from __future__ import absolute_import
from bs4 import BeautifulSoup
from datetime import datetime
import re
from celery import shared_task
from ozon_products import constants
from ozon_products.models import Products

# from ozon_parser.celery import app
# from django.core.cache import cache
import parsing_manage_bot
#
# import constants
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--headless=new")
driver = webdriver.Chrome(options=chrome_options)

URL = constants.URL
MAX_NUM = constants.MAX_NUM
DEFAULT_NUM = constants.DEFAULT_NUM
Per_PAGE = constants.Per_PAGE


@shared_task
def get_products(num=DEFAULT_NUM):
    products = []
    num = MAX_NUM if num > MAX_NUM else num
    full_page_count, n = num // Per_PAGE, num % Per_PAGE
    for page in range(full_page_count):
        products.extend(parse_products(Per_PAGE, page + 1))
    products.extend(parse_products(n, full_page_count + 1))

    current_date = datetime.now()
    products = [Products(code=product["code"], link=product["link"], title=product["title"], price=product["price"],
                         description=product["description"], image_url=product["image_url"],
                         discount=product["discount"], date=current_date) for product in products]
    # Сохраняем полученные продукты в БД, обновляя данные тех, которые в базе уже есть
    try:
        Products.objects.bulk_create(products, update_conflicts=True,
                                     update_fields=["link", "title", "price", "description", "image_url",
                                                    "discount", "date"])
        mess = f"Задача на парсинг товаров с сайта Ozon завершена. В БД сохранено товаров: {len(products)}"

    except:
        mess = "Парсинг завершен. Произошла ошибка добавления в БД данных, полученных с сайта Озон"
        print("Ошибка добавления данных в БД")
    parsing_manage_bot.send_parsing_notify(mess)
    return True


def parse_products(n, page=1):
    parsed_products = []
    url = URL + '?page={}'.format(page)
    # Получаем содержимое страницы с товарами
    content = get_content(url)
    html = BeautifulSoup(content, 'html.parser')
    try:
        for div in html.find_all('div', class_='i9j ik')[:n]:
            link = "https://www.ozon.ru" + div.find('a')['href']
            title = div.find('span', class_='tsBody500Medium').text.strip()
            image_url = div.find('img', class_='c9-a')['src']

            # Получаем содержимое страницы конкретного товара
            product_content = get_content(link)
            product_html = BeautifulSoup(product_content, 'html.parser')
            text_code = product_html.find('span', class_='v0j j1v').text
            code = int(re.sub("[^0-9]", "", text_code))
            text_price = product_html.find('span', class_='sk').text.strip().split()[0]
            price = float(re.sub(",", ".", text_price))
            try:
                discount = product_html.find('div', class_='d0r').span.text.strip()
            except:
                discount = ""
            try:
                description = product_html.find('div', class_='ra-a1').text.strip()
            except:
                description = ""

            parsed_products.append(
                {"code": code, "link": link, "title": title, "price": price, "description": description,
                 "image_url": image_url, "discount": discount})
    except Exception as e:
        print(e)

    return parsed_products


def get_content(url):
    # Получаем страницу
    driver.get(url)
    try:
        # Ждем пока не появится на странице тэг с id ozonTagManagerApp
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ozonTagManagerApp"))
        )
    finally:
        # Возвращаем текст страницы
        return driver.page_source

