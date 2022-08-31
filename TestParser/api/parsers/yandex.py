import unicodedata
import requests
import logging

from bs4 import BeautifulSoup

logging.getLogger(__name__).setLevel(logging.INFO)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
}


def get_html(url):
    request = requests.get(url, headers=HEADERS)
    if request.ok:
        return request.text
    logging.warning(f'Request to {url} completed with code {request.status_code}')


def parse_yandex(url):
    page = get_html(url)
    soup = BeautifulSoup(page, "lxml")
    news_list = soup.findAll('div', class_='news-list__item')
    if news_list is not None:
        clear_news_data = []
        for item in news_list[:10]:
            post_url = item.find_next('a', href=True)['href'].replace('/partners/news', '')
            description, tags = parse_description_and_tags(url + post_url)
            clear_news_data.append(
                {
                    "header": unicodedata.normalize(
                        "NFKD", item.findNext('div', class_='news-list__item-header').text
                    ),
                    "description": unicodedata.normalize("NFKD", description),
                    "meta": item.findNext('time', class_='news-list__item-date')['datetime']
                    ,
                    "tags": tags
                }
            )
        return clear_news_data
    else:
        logging.warning('Data was not found during parsing website')


def parse_description_and_tags(url):
    page = get_html(url)
    soup = BeautifulSoup(page, "lxml")
    raw_tags = soup.findAll('a', class_='link link_theme_light-gray news-info__tag i-bem')
    description = soup.find('div', class_='news-info__post-body html-content page-content')
    if raw_tags is not None:
        tags = []
        for item in raw_tags:
            tags.append(item.text)
    else:
        tags = raw_tags
    if description is not None:
        description = description.text
    return description, tags
