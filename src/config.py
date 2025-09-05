from decouple import config


db_name = config('DB_NAME')
postgres_user = config('POSTGRES_USER')
postgres_password = config('POSTGRES_PASSWORD')
host_name = config('HOST_NAME')
port = config('PG_PORT')
schema_name = config('SCHEMA_NAME')
table_name = config('TABLE_NAME')

enable_api_docs = config('ENABLE_API_DOCS', cast=bool)

uvicorn_logging_level = config('UVI_LOGGING_LEVEL')

logging_level = config('LOGGING_LEVEL')
