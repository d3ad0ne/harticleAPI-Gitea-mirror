import DBwork
from DBmodel import db
import scraper
from fastapi import Response, status, APIRouter
from pydantic import BaseModel
import psycopg2
import base64


router = APIRouter(prefix='/api')


class Entry(BaseModel):
    username: str
    url: str
    rating: int | None = None


class Article(BaseModel):
    url: str 


class Amount(BaseModel):
    amount: int


@router.get('/ping')
async def ping():
    return {'message': 'pong'}


@router.get('/rates')
async def get_rates():
    result = DBwork.get_all_entries(db.connection)
    return result


@router.post('/article/rate')
async def save_rating(entry: Entry, response: Response):
    try:
        DBwork.add_entry(article_url=entry.url, 
                        rating=entry.rating, 
                        connection=db.connection
                        )
        message = 'success'
    except psycopg2.Error:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        message = 'internal server error'
    finally:
        return {'message': message,
                'username': entry.username,
                'url': entry.url,
                'rating': entry.rating
                }


@router.post('/article/remove_rate')
async def remove_rating(entry: Entry, response: Response):
    try:
        DBwork.delete_entry(entry.url, db.connection)
        message = 'success'
    except psycopg2.Error:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        message = 'internal server error'
    finally:
        return {'message': message}


@router.post('/article/get/html')
async def get_article_html(article: Article, response: Response = None):
    html_string = await scraper.get_article_html(article.url)
    b64_string = base64.b64encode(html_string.encode('utf-8')).decode('utf-8')
    return {article.url: b64_string}


@router.post('/article/get/md')
async def get_article_md(article: Article, response: Response = None):
    md_string = await scraper.get_article_html(article.url, md=True)
    b64_string = base64.b64encode(md_string.encode('utf-8')).decode('utf-8')
    return {article.url: b64_string}


@router.post('/articles/get/html')
async def get_n_articles_html(amount: Amount, response: Response = None):
    articles = {}
    urls = await scraper.get_articles_from_feed(amount.amount)
    for url in urls:
        html = await scraper.get_article_html(f'https://habr.com{url}')
        b64_string = base64.b64encode(html.encode('utf-8')).decode('utf-8')
        articles[f'https://habr.com{url}'] = b64_string
    return articles


@router.post('/articles/get/md')
async def get_n_articles_md(amount: Amount, response: Response = None):
    articles = {}
    for url in await scraper.get_articles_from_feed(amount.amount):
        md = await scraper.get_article_html(f'https://habr.com{url}', md=True)
        b64_string = base64.b64encode(md.encode('utf-8')).decode('utf-8')
        articles[f'https://habr.com{url}'] = b64_string
    return articles
