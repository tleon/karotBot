#! python3

import requests
from bs4 import BeautifulSoup


class Spider:
    def __init__(self, url):
        self.url = url
        self.short_news = self.parse_news()

    @staticmethod
    def fetch_url(url):
        return requests.get(url)

    def parse_news(self):
        soup = BeautifulSoup(self.fetch_url(self.url).content, 'lxml')
        return soup.find_all(attrs={"class": "news"})

    def parse_article(self, article_link):
        soup = BeautifulSoup(self.fetch_url(article_link).content, 'lxml')
        pass
