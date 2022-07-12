FROM python:3.10-bullseye

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY Pipfile Pipfile.lock /usr/src/app/
RUN pip install --upgrade pip
RUN pip install pipenv && pipenv install --system

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV LANG en_GB.UTF-8
ENV PYTHONIOENCODING utf_8

RUN apt-get update && apt-get install -y \
        gettext \
    --no-install-recommends
