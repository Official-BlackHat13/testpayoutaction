# FROM python:3
# ENV PYTHONUNBUFFERED 1
# RUN mkdir /code
# WORKDIR /code
# ADD requirements.txt /code/
# RUN pip install pymysql
# RUN apt update && apt install vim
# # RUN apt install vim
# RUN pip install -r requirements.txt
# ADD . /code/

FROM python:3.9-slim

COPY --from=openjdk:8-jre-slim /usr/local/openjdk-8 /usr/local/openjdk-8

ENV JAVA_HOME /usr/local/openjdk-8

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code

ADD ./requirements.txt /app/requirements.txt

ADD . /code/
RUN chmod +x ./script.sh

RUN pip install -r requirements.txt
RUN pip install gunicorn
RUN apt -y update && apt install  -y vim
RUN pip install pymysql gevent requests tabulate
EXPOSE 8000 8081
#CMD ["./script.sh"]



