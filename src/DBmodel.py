import psycopg2


class DataBase:
    connection: psycopg2._psycopg.connection | None = None

db = DataBase()
