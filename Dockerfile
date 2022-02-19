# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /national-rail-query-service

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

ENV PYTHONPATH="$PYTHONPATH:/national-rail-query-service"

CMD python3 src/service/app.py

