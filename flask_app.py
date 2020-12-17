# Author : Frances Anastasia 
# Production Server for incoming Foil Requests
# A service provided by Williamson Law Book Company 

import re
import os
import sys
import json
import time 
import uuid
import subprocess

from waitress import serve
from flask_cors import CORS
from datetime import datetime
from flaskext.mysql import MySQL

from passlib.hash import md5_crypt

from flask import Flask, jsonify, request, redirect, url_for, render_template, send_from_directory 

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