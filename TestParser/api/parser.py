import unicodedata
import requests
import logging

from bs4 import BeautifulSoup

logging.getLogger(__name__).setLevel(logging.INFO)


def get_html(url):
    request = requests.get(url)
    if request.ok:
        logging.warning(f'Request to {url} completed with code {request.status_code}')
        return request.text


def parse_news(url):
    page = get_html(url)
    soup = BeautifulSoup(page, "lxml")
    news_list = soup.findAll('div', class_='news-list__item')
    if news_list is not None:
        clear_news_data = []
        for item in news_list[:10]:
            post_url = item.find_next('a', href=True)['href'].replace('/partners/news', '')
            clear_news_data.append(
                {
                    "header": unicodedata.normalize(
                        "NFKD", item.findNext('div', class_='news-list__item-header').text
                    ),
                    "description": unicodedata.normalize(
                        "NFKD", item.findNext('div', class_='news-list__item-description').text
                    ),
                    "meta": item.findNext('time', class_='news-list__item-date')['datetime']
                    ,
                    "tags": parse_tags(url + post_url)
                }
            )
        return clear_news_data
    else:
        logging.warning('Data was not found during parsing website')


def parse_tags(url):
    page = get_html(url)
    soup = BeautifulSoup(page, "lxml")
    tags_list = soup.findAll('a', class_='link link_theme_light-gray news-info__tag i-bem')
    if tags_list is not None:
        clear_news_data = []
        for item in tags_list:
            clear_news_data.append(item.text)
        return clear_news_data


# def main():
#     url = 'https://market.yandex.ru/partners/news'
#     print(parse_news(url))
#
#
# if __name__ == '__main__':
#     main()
