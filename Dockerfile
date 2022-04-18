FROM python:3.8

ENV PYTHONUNBUFFERED 1

ENV APP_ROOT /goodgame

WORKDIR ${APP_ROOT}

RUN apt-get update

RUN pip3 install -U pip

COPY requirements.txt ${APP_ROOT}/requirements.txt

RUN pip3 install -r ${APP_ROOT}/requirements.txt

WORKDIR ${APP_ROOT}

ADD . ${APP_ROOT}

RUN chmod 775 -R ${APP_ROOT}