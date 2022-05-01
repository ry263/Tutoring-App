FROM python:3.7-slim

RUN mkdir usr/app
WORKDIR usr/app

COPY . .

RUN pip install -r requirements.txt
CMD python app.py
#CMD python pa4_test.py to test the -slim version