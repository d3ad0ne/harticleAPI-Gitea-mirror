import asyncio
import APIapp
import uvicorn


asyncio.run(APIapp.main())
uvicorn.run("APIapp:app", host="127.0.0.1", port=8000, log_level="info")