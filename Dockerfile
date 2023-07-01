FROM python:3.9-slim

ADD /app /app

COPY requirements.txt /

WORKDIR /

RUN pip3 install -r requirements.txt

CMD exec gunicorn -b :80 -w 1 app:app