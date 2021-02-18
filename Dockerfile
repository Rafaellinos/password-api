FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    netcat \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /app

COPY . ./

RUN pip3 install -r requirements.txt

RUN mv ./entrypoint.sh /

ENTRYPOINT ["/entrypoint.sh"]