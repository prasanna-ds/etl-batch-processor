FROM python:3.6.6-alpine3.8

LABEL Prasanna prasanna.sudhindrakumar@gmail.com

RUN apk --no-cache --update-cache add gcc gfortran bash python python-dev py-pip build-base wget freetype-dev libpng-dev openblas-dev
WORKDIR /app

COPY Pipfile ./
COPY Pipfile.lock ./

RUN pip install --upgrade pip \
    && pip install --no-cache-dir pipenv \ 
    && pipenv install --system --deploy

COPY . /app
# COPY . ./
# RUN cd /app

CMD python app.py --env=${APP_ENV}