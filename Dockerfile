FROM python:3.12.2-slim-bullseye

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["sh", "entrypoint.sh"]