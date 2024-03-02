FROM python:3.10

LABEL authors="arsen"

ENV PYTHONWRITEBYTECODE 1

RUN mkdir /Forex

WORKDIR /Forex/

COPY requirements.txt .

RUN pip install -r /Forex/requirements.txt

COPY . /Forex