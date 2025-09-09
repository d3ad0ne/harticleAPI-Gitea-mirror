import config
import router
import DBwork
from DBmodel import db
from fastapi import FastAPI
from loguru import logger
from contextlib import asynccontextmanager


if config.enable_api_docs:
    docs_url = '/api/docs'
else:
    docs_url = None

schema_name = 'harticle'
table_name = 'articles'


@asynccontextmanager
async def lifespan(app: FastAPI):
    DBwork.set_connection()
    DBwork.schema_creator(schema_name, db.connection)
    DBwork.table_creator(schema_name, table_name, db.connection)    
    yield
    DBwork.close_connection(db.connection)


app = FastAPI(docs_url=docs_url, lifespan=lifespan)


def create_app():
    logging_level = config.logging_level
    logger.add(
    "sys.stdout",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {file}:{line} - {message}",
    colorize=True,
    level=logging_level
    )
    
    app.include_router(router.router)

    return app
