FROM python:3.11.9-alpine3.19

RUN apk update && apk add python3-dev \
                        gcc \
                        libc-dev \
                        libffi-dev \
                        openssl-dev \
                        libxml2-dev \
                        build-base \
                        postgresql-dev


RUN pip install  --no-cache-dir --upgrade setuptools poetry pyopenssl

WORKDIR /application
RUN cd /application
COPY poetry.lock pyproject.toml alembic.ini mypy.init pytest.ini ./

RUN poetry config virtualenvs.create false
RUN poetry install

COPY . .