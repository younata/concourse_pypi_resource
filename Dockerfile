FROM python:latest

ADD bin /opt/resource
ADD . /opt/lib/

RUN pip install /opt/lib
