from bs4 import BeautifulSoup
import requests
import re
from markdownify import MarkdownConverter
from loguru import logger


async def get_article_html(url: str, md: bool = False) -> str:
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        content = soup.find('div', class_='tm-article-presenter')
        # style = soup.find('style')
        filter_tags = ['footer', 'meta', 'widget', 'vote', 'hubs', 'sticky']
        for tag in filter_tags:
            trash = content.find_all(class_=re.compile(tag))
            for element in trash:
                element.decompose()
        if md:
            return MarkdownConverter().convert_soup(content)
        else:
            return content.prettify()
    else:
        logger.error(f'Error during fetching habr response. Status code: {response.status_code}')


async def get_articles_from_feed(amount: int) -> list[str]:
    response = requests.get('https://habr.com/ru/feed/')
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        urls = []
        for url in soup.find_all(class_='tm-title__link', limit=amount, href=True):
            urls.append(str(url['href']))
        return urls
    else:
        logger.error(f'Error during fetching habr response. Status code: {response.status_code}')
