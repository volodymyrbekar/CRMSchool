FROM python:3.12.2-slim-bullseye

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
ENTRYPOINT ["sh", "entrypoint.sh"]