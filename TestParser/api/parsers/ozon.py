import datetime
import json
import unicodedata
import requests
import logging

from bs4 import BeautifulSoup

logging.getLogger(__name__).setLevel(logging.INFO)


with open('headers.json', 'r') as json_file:
    headers = json.load(json_file)


def get_html(url):
    request = requests.get(url, headers=headers)
    if request.ok:
        return request.text
    logging.warning(f'Request to {url} completed with code {request.status_code}')


def parse_ozon(url):
    page = get_html(url)
    soup = BeautifulSoup(page, "lxml")
    news_list = soup.findAll('div', class_='news-card')
    if news_list is not None:
        clear_news_data = []
        for item in news_list[:10]:
            post_url = item.find_next('a', href=True)['href'].replace('/news', '')
            description, tags = parse_description_and_tags(url + post_url)
            date = format_date(item.findNext('span', class_='news-card__date').text)
            clear_news_data.append(
                {
                    "header": unicodedata.normalize(
                        "NFKD", item.findNext('h3', class_='news-card__title').text.strip()
                    ),
                    "description": unicodedata.normalize("NFKD", description),
                    "meta": date,
                    "tags": tags
                }
            )
        return clear_news_data
    else:
        logging.warning('Data was not found during parsing website')


def parse_description_and_tags(url):
    page = get_html(url)
    soup = BeautifulSoup(page, "lxml")
    tags = soup.find('div', class_='page-info__topic-value')
    description = soup.find('section', class_='new-section html-content_Ol8P9')
    if tags is not None:
        tags = tags.text.strip().split(", ")
    if description is not None:
        description = description.text
    return description, tags


def format_date(date):
    RU_MONTH_VALUES = {
        'января': 1,
        'февраля': 2,
        'марта': 3,
        'апреля': 4,
        'мая': 5,
        'июня': 6,
        'июля': 7,
        'августа': 8,
        'сентября': 9,
        'октября': 10,
        'ноября': 11,
        'декабря': 12,
    }
    for k, v in RU_MONTH_VALUES.items():
        date = date.replace(k, str(v))
    date = date + " " + str(datetime.datetime.now().year)
    formatted_date = datetime.datetime.strptime(date, '%d %m %Y')
    formatted_date.replace(year=datetime.datetime.now().year, hour=0, minute=0, second=0)
    return formatted_date
