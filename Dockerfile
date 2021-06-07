FROM python:3.8.10

WORKDIR /code/

# copy and install requirements first to leverage caching
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# copy the actual code
COPY . /code/

# with right access
RUN chmod u+rwx ./manage.py

# For End user
# RUN chmod go+rx filename.py


CMD ./manage.py runserver 0.0.0.0:8000