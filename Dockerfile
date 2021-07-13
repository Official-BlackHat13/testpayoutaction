FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install pymysql
RUN apt update && apt install vim
# RUN apt install vim
RUN pip install -r requirements.txt
ADD . /code/
                                                                                                                                     
