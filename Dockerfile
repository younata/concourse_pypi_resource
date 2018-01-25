FROM python:latest

ADD bin /opt/resource
ADD lib /opt/lib

RUN pip install /opt/lib
