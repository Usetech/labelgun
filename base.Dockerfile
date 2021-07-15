FROM python:3.8.6-slim-buster

ARG CURRENT_ENV=prod
ENV POETRY_VERSION=1.1.5

WORKDIR /opt/app/
COPY ./pyproject.toml ./poetry.lock /opt/app/

RUN apt-get update \
    && apt-get install -y wget git \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && ln -s /root/.poetry/bin/poetry /usr/bin/poetry \
    && wget https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py \
    && python ./get-poetry.py --version $POETRY_VERSION \
    && poetry config virtualenvs.create false \
    && /bin/bash -c 'poetry install $(test "$CURRENT_ENV" == prod && echo "--no-dev") --no-interaction --no-ansi' \
    && rm ./get-poetry.py \
    && apt-get purge -y wget \
    && apt autoremove -y \
    && apt autoclean -y \
    && rm -fr /var/lib/apt/lists /var/lib/cache/* /var/log/*
