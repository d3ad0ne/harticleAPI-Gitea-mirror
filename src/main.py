import router
import uvicorn
from loguru import logger
import config
from fastapi import FastAPI


logging_level = config.logging_level
logger.add(
    "sys.stdout",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {file}:{line} - {message}",
    colorize=True,
    level=logging_level
)

if config.enable_api_docs:
    docs_url = '/api/docs'
else:
    docs_url = None

app = FastAPI(docs_url=docs_url)
app.include_router(router.router)

    
router.main()
uvicorn.run(app=app, host="127.0.0.1", port=8000, log_level="info")
