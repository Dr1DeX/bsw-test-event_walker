FROM python:3.12-slim

WORKDIR /line-provider

COPY /pyproject.toml .

RUN pip install poetry

COPY /line-provider .
