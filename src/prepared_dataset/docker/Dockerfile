FROM python:3
LABEL maintainer="Nicolas Wolf <nicolas.wolf@fau.de>"

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

# CMD uwsgi --ini uwsgi.ini
CMD python3 api.py