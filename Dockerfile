FROM registry.usetech.ru/pub/labelgun/ci:base

ARG CURRENT_ENV=${CURRENT_ENV}

COPY ./pyproject.toml ./poetry.lock /opt/app/
WORKDIR /opt/app/
RUN /bin/bash -c 'poetry install $(test "$CURRENT_ENV" == prod && echo "--no-dev") --no-interaction --no-ansi -E logger'
