import psycopg2
import config
from loguru import logger


logging_level = config.logging_level
logger.add(
    "sys.stdout",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {file}:{line} - {message}",
    colorize=True,
    level=logging_level
)


#connection stuff
def set_connection():
    try:
        connection = psycopg2.connect(
        dbname = config.db_name,
        user = config.postgres_user,
        password = config.postgres_password,
        host = config.host_name,
        port = config.port
        )
        cursor = connection.cursor()
        return connection, cursor
    except psycopg2.Error as e:
        logger.error(f'Failed to set connection to the PostgreSQL DB: {e.pgerror}')


def close_connection(connection, cursor):
    try:
        cursor.close()
        connection.close()
    except psycopg2.Error as e:
        logger.error(f'Failed to close PostgreSQL connection: {e.pgerror}')


#actual DB alters
def add_entry(article_url, rating):
    connection, cursor = set_connection()
    try:
        cursor.execute("INSERT INTO harticle.articles (article_url, rating) VALUES (%s, %s);", (article_url, rating,))
        connection.commit()
        logger.info('An entry has been written to the PGSQL DB successfully')
    except psycopg2.Error as e:
        logger.error(f'Failed to write an entry for article \'{article_url}\': {e.pgerror}')
    finally:
        close_connection(connection, cursor)


def delete_entry(article_url, connection, cursor):
    connection, cursor = set_connection()
    try:
        cursor.execute("DELETE FROM harticle.articles WHERE article_url = %s;", (article_url,))
        connection.commit()
        logger.info(f'Rating for article \'{article_url}\' was cleared successfully')
    except psycopg2.Error as e:
        logger.error(f'Failed to clear a rating entry for article \'{article_url}\': {e.pgerror}')
    finally:
        close_connection(connection, cursor)


# def delete_rating(article_url, connection, cursor):
#     close_connection(connection, cursor)
#     try:
#         cursor.execute("UPDATE harticle.articles SET rating = NULL WHERE article_url = %s;", (article_url,))
#         connection.commit()
#         logger.info(f'Rating for article \'{article_url}\' was cleared successfully')
#         close_connection(connection, cursor)
#     except psycopg2.Error as e:
#         logger.error(f'Failed to clear a rating entry for article \'{article_url}\': {e.pgerror}')


def get_all_entries():
    connection, cursor = set_connection()
    try:
        cursor.execute('SELECT article_url, rating FROM harticle.articles;')
        entries = cursor.fetchall()
        logger.info('All entry pairs have been retrieved successfully')
        return entries
    except psycopg2.Error as e:
        logger.error(f'Failed to fetch DB entries: {e.pgerror}')
    finally:
        close_connection(connection, cursor)


#'create if no any' type functions for schema and table
def schema_creator(schema_name):
    conn, cur = set_connection()
    try:
        cur.execute(f'CREATE SCHEMA IF NOT EXISTS {schema_name};')
        conn.commit()
        logger.info(f'Successfully created schema {schema_name} if it didn\'t exist yet')
    except psycopg2.Error as e:
        logger.error(f'Error during schema creation: {e}')
    finally:
        close_connection(conn, cur)


def table_creator(schema_name, table_name):
    conn, cur = set_connection()
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
        conn.commit()
        logger.info(f'Successfully created table {table_name} in schema {schema_name} if it didn\'t exist yet')
    except psycopg2.Error as e:
        logger.error(f'Error during table creation: {e}')
    finally:
        close_connection(conn, cur)