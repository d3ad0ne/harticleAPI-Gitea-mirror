import DBwork
from fastapi import FastAPI, Response, status
from pydantic import BaseModel
import psycopg2
from json import dumps


schema_name = 'harticle'
table_name = 'articles'

app = FastAPI()

class Entry(BaseModel):
    url: str
    rating: int | None = None


@app.get('/api/ping')
async def ping():
    return {'message': 'pong'}


@app.get('/api/rates')
async def get_rates():
    return dumps(DBwork.get_all_entries())


@app.post('/api/article/rate')
async def save_rating(entry: Entry, response: Response):
    conn, cur = DBwork.set_connection()
    try:
        DBwork.add_entry(article_url=entry.url, 
                        rating=entry.rating, 
                        connection=conn, 
                        cursor=cur
                        )
        message = 'success'
    except psycopg2.Error:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        message = 'internal server error'
    finally:
        DBwork.close_connection(conn, cur)
        return {'message': message,
                'url': entry.url,
                'rating': entry.rating
                }
    

@app.post('/api/article/remove_rate')
async def remove_rating(entry: Entry, response: Response):
    conn, cur = DBwork.set_connection()
    try:
        DBwork.delete_entry(entry.url, conn, cur)
        message = 'success'
    except psycopg2.Error:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        message = 'internal server error'
    finally:
        DBwork.close_connection(conn, cur)
        return {'message': message}


@app.post('/api/articles/get')
async def megafunc(entry: Entry, response: Response):
    ...


'''   MAIN   '''
async def main():
    DBwork.schema_creator(schema_name)
    DBwork.table_creator(schema_name, table_name)

