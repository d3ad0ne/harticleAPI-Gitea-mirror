from decouple import config


db_name = config('DB_NAME')
postgres_user = config('POSTGRES_USER')
postgres_password = config('POSTGRES_PASSWORD')
host_name = config('HOST_NAME')
port = config('PORT')
logging_level = config('LOGGING_LEVEL')
enable_api_docs = config('ENABLE_API_DOCS', cast=bool)
