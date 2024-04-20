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
COPY poetry.lock pyproject.toml ./
COPY . .
COPY config.env config.dev.env

RUN poetry config virtualenvs.create false
RUN poetry install

CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
