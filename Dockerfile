# Base Dockerfile for TICKETSMITH backend
FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

CMD ["python", "ticketsmith_cli.py"]
