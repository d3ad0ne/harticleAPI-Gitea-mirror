import DBwork
import scraper
from fastapi import Response, status, APIRouter
from pydantic import BaseModel
import psycopg2
from json import dumps


schema_name = 'harticle'
table_name = 'articles'

router = APIRouter(prefix='/api')

class Entry(BaseModel):
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
    conn = DBwork.set_connection()
    result = dumps(DBwork.get_all_entries(conn))
    DBwork.close_connection(conn)
    return result


@router.post('/article/rate')
async def save_rating(entry: Entry, response: Response):
    conn = DBwork.set_connection()
    try:
        DBwork.add_entry(article_url=entry.url, 
                        rating=entry.rating, 
                        connection=conn
                        )
        message = 'success'
    except psycopg2.Error:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        message = 'internal server error'
    finally:
        DBwork.close_connection(conn)
        return {'message': message,
                'url': entry.url,
                'rating': entry.rating
                }
    

@router.post('/article/remove_rate')
async def remove_rating(entry: Entry, response: Response):
    conn = DBwork.set_connection()
    try:
        DBwork.delete_entry(entry.url, conn)
        message = 'success'
    except psycopg2.Error:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        message = 'internal server error'
    finally:
        DBwork.close_connection(conn)
        return {'message': message}


@router.post('/article/get/html')
async def get_article_html(article: Article, response: Response = None):
    html_string = await scraper.get_article_html(article.url, md=False)
    return html_string
    
    
@router.post('/article/get/md')
async def get_article_md(article: Article, response: Response = None):
    md_string = await scraper.get_article_html(article.url, md=True)
    return md_string
    
    
@router.post('/articles/get/html')
async def get_n_articles_html(amount: Amount, response: Response = None):
    articles = []
    for url in await scraper.get_articles_from_feed(amount.amount):
        articles.append(await scraper.get_article_html(f'https://habr.com{url}'))
    return articles


@router.post('/articles/get/md')
async def get_n_articles_md(amount: Amount, response: Response = None):
    articles = []
    for url in await scraper.get_articles_from_feed(amount.amount):
        articles.append(await scraper.get_article_md(f'https://habr.com{url}'))
    return articles


'''   MAIN   '''
def main():
    DBwork.schema_creator(schema_name)
    DBwork.table_creator(schema_name, table_name)
