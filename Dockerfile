FROM python:3.8

RUN apt-get install libpq-dev

COPY ./app /app
COPY requirements.txt /tmp
COPY ./alembic.ini /
COPY ./entrypoint.sh /

RUN pip3 install -r /tmp/requirements.txt

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]