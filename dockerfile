FROM python:3.13-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev build-essential

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "src/main.py"]
