import psycopg2
import config
from loguru import logger


#connection stuff
connection = None

def set_connection():
    global connection
    try:
        connection = psycopg2.connect(
        dbname = config.db_name,
        user = config.postgres_user,
        password = config.postgres_password,
        host = config.host_name,
        port = config.port
        )
        logger.info('Connection to PostreSQL DB set successfully')
    except psycopg2.Error as e:
        logger.error(f'Failed to set connection to the PostgreSQL DB: {e.pgerror}')


def close_connection(connection):
    try:
        cursor = connection.cursor()
        cursor.close()
        connection.close()
        logger.info('Connection to PostreSQL DB closed successfully')
    except psycopg2.Error as e:
        logger.error(f'Failed to close PostgreSQL connection: {e.pgerror}')


#actual DB alters
def add_entry(article_url, rating, connection):
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO harticle.articles (article_url, rating) VALUES (%s, %s);", (article_url, rating,))
        connection.commit()
        logger.info('An entry has been written to the PGSQL DB successfully')
    except psycopg2.Error as e:
        logger.error(f'Failed to write an entry for article \'{article_url}\': {e.pgerror}')


def delete_entry(article_url, connection):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM harticle.articles WHERE article_url = %s;", (article_url,))
        connection.commit()
        logger.info(f'Rating for article \'{article_url}\' was cleared successfully')
    except psycopg2.Error as e:
        logger.error(f'Failed to clear a rating entry for article \'{article_url}\': {e.pgerror}')


# def delete_rating(article_url, connection):
#     try:
#         cursor = connection.cursor()
#         cursor.execute("UPDATE harticle.articles SET rating = NULL WHERE article_url = %s;", (article_url,))
#         connection.commit()
#         logger.info(f'Rating for article \'{article_url}\' was cleared successfully')
#     except psycopg2.Error as e:
#         logger.error(f'Failed to clear a rating entry for article \'{article_url}\': {e.pgerror}')


def get_all_entries(connection):
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT article_url, rating FROM harticle.articles;')
        entries = cursor.fetchall()
        logger.info('All entry pairs have been retrieved successfully')
        return entries
    except psycopg2.Error as e:
        logger.error(f'Failed to fetch DB entries: {e.pgerror}')


#'create if no any' type functions for schema and table
def schema_creator(schema_name, connection):
    cur = connection.cursor()
    try:
        cur.execute(f'CREATE SCHEMA IF NOT EXISTS {schema_name};')
        connection.commit()
        logger.info(f'Successfully created schema {schema_name} if it didn\'t exist yet')
    except psycopg2.Error as e:
        logger.error(f'Error during schema creation: {e}')



def table_creator(schema_name, table_name, connection):
    cur = connection.cursor()
    try:
        cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {schema_name}.{table_name}
        (
            id SERIAL PRIMARY KEY,
            article_url VARCHAR(3000) UNIQUE NOT NULL,
            rating INT CHECK (rating < 2)
        )

        TABLESPACE pg_default;

        ALTER TABLE IF EXISTS {schema_name}.{table_name}
            OWNER to {config.postgres_user};
        ''')
        connection.commit()
        logger.info(f'Successfully created table {table_name} in schema {schema_name} if it didn\'t exist yet')
    except psycopg2.Error as e:
        logger.error(f'Error during table creation: {e}')

