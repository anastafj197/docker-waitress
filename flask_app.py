from flask import Flask, render_template
from waitress import serve

import uuid
import os
import re

app = Flask(__name__)

@app.after_request
def add_hostname_header(response):
    env_host = str(os.environ.get('HOSTNAME'))
    hostname = re.findall('[a-z]{3}-\d$', env_host)
    if hostname:
            response.headers["SP-LOCATION"] = hostname
    return response

@app.route('/')
def get_uuid():
    return str(uuid.uuid4())

if __name__ == '__main__':
	serve(app, listen='*:80')