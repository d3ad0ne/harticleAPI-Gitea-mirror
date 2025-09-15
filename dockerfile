FROM pythoFROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev build-essential

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "src/main.py"]
