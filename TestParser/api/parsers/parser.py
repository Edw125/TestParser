from api.parsers.ozon import parse_ozon
from api.parsers.yandex import parse_yandex


def parse_news(url):
    yandex = 'https://market.yandex.ru/partners/news'
    ozon = 'https://seller.ozon.ru/news'
    if url == yandex:
        return parse_yandex(url)
    elif url == ozon:
        return parse_ozon(url)
