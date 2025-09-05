import uvicorn
from config import uvicorn_logging_level
from app_creator import create_app


if __name__ == '__main__':
    app = create_app()
    uvicorn.run(app=app, host="127.0.0.1", port=8000, log_level=uvicorn_logging_level.lower())
