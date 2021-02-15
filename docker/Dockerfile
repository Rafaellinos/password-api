FROM python:3.8

RUN apt-get install libpq-dev

COPY ../app /

RUN pip3 install /requirements.txt

WORKDIR /app

CMD ["python3 main.py"]