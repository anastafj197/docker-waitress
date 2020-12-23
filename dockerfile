FROM python:3.6.1-alpine

WORKDIR /api

ADD . /api

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "foil_server.py"]