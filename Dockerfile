FROM python:3.9-slim



ADD ./requirements.txt /app/requirements.txt




ADD . /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN pip install gunicorn
RUN apt -y update && apt install  -y vim
RUN pip install pymysql
RUN pip install paytmchecksum 
RUN pip install gevent
EXPOSE 9000

CMD ["gunicorn", "--bind", ":80", "--timeout", "200", "--workers", "30", "--threads", "30", "--worker-connections", "1000", "--worker-class", "gevent", "payout.wsgi"]

