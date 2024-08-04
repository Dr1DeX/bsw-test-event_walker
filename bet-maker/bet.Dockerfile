FROM python:3.12-slim

WORKDIR /bet-maker

COPY /pyproject.toml .

RUN pip install poetry
RUN poetry install

COPY /bet-maker .