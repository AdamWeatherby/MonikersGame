FROM ubuntu:16.04

RUN apt-get update -y && apt-get install -y python-pip python-dev

RUN apt-get install -y gunicorn 

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

CMD  gunicorn -w 4 -b 0.0.0.0:4000 main:application
