FROM python:3.12


SHELL ["/bin/bash", "-c"]

ENV PYTHONUNBUFFERED 1


RUN pip install --upgrade pip
RUN apt update && apt -qy install gcc libjpeg-dev libxslt-dev \
    libpq-dev cron openssh-client vim locales python3-dev postgresql

WORKDIR /project

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

