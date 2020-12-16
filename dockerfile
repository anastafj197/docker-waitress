FROM python:3.6.1-alpine

WORKDIR /project

ADD . /project

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python","flask_app.py"]