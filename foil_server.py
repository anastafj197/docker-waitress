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
mysql = MySQL()

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# DB Connectivity Inforamtion 
app.config['MYSQL_DATABASE_USER'] = 'frank'
app.config['MYSQL_DATABASE_PASSWORD'] = 'NKA&Sg@#Ddad3yH'
app.config['MYSQL_DATABASE_DB'] = 'foil'
app.config['MYSQL_DATABASE_HOST'] = '192.168.1.196'

mysql.init_app(app)

CORS(app)

cors = CORS(app, resources={r"/": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

conn = mysql.connect()
cursor = conn.cursor()

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

@app.route('/request', methods=['POST', 'GET'])
def process_request():
  print("request received")

  req_data = request.get_json(force=True)

  f_name  = req_data['f_name']
  b_name  = req_data['b_name']
  email   = req_data['email']
  phone   = req_data['phone']
  fax     = req_data['fax']
  address = req_data['address']
  town    = req_data['town']
  state   = req_data['state']
  zipcode = req_data['zip']
  pertaining = req_data['pertaining']
  details = req_data['details']
  chain = req_data['chain']

  now = datetime.now()
  current_time = now.strftime("%H:%M %m/%d/%Y")

  print(town)

  town = town[0].upper() + town[1].upper() + town[2:]

  print(town)

  cursor.execute("SELECT regnum FROM users WHERE muni LIKE %s", (town))
  value = cursor.fetchone()
  regnum = json.dumps(value)
  regnum = regnum.replace('"', "")
  regnum = regnum.replace('[', "")
  regnum = regnum.replace(']', "")
  print(regnum)

    # This line needs regnum added 
  cursor.execute("INSERT INTO `requests` VALUES (0, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0)", (regnum, f_name, b_name, email, phone, fax, address, town, state, zipcode, pertaining, details, chain, current_time))

  conn.commit()

  cursor.execute("SELECT email FROM users WHERE muni LIKE %s", (town))
  value = cursor.fetchone()
  email = json.dumps(value)
  email = email.replace('"', "")
  email = email.replace('[', "")
  email = email.replace(']', "")
  print("sending email to - " + email)

  auto_emailer.send_clerk_email(email)

  print("DB entry complete")

  return ('xxx', 204)

@app.route('/login', methods=['POST', 'GET'])
def login():
  print("login page")

  req_data = request.get_json(force=True)

  u_name = req_data['u_name']
  p_word = req_data['p_word']

  print(u_name, p_word)

  cursor.execute("SELECT regnum, name, muni FROM users WHERE username = %s AND password = %s", (u_name, p_word))
  value = cursor.fetchone()
  j_value = json.dumps(value)

  return (j_value)


@app.route('/get_munis', methods=['POST', 'GET'])
def get_munis():
  print("Grabbing munis")

  cursor.execute("SELECT muni from users")

  value = cursor.fetchall()
  j_value = json.dumps(value)

  print(j_value)

  return (j_value)

# This route returns an array of department names specific to the payload (regnum) 
# Lots of string manipulation involved to get the data in the correct format
@app.route('/get_deps', methods=['POST', 'GET'])
def get_deps():
  print("Grabbing Departments")

  req_data = request.get_json(force=True)

  regnum = req_data['regnum']

  index_array = []
  to_return = []
  print("1")
  time.sleep( 1 )
  cursor.execute("SELECT Column_name FROM Information_schema.columns WHERE Table_name LIKE 'departments';")
  time.sleep( 1 )
  print("2")

  # a for all departments
  a_deps = cursor.fetchall()
  a_deps = json.dumps(a_deps, default = str)

  print("3")

  a_stripped = a_deps.replace('[', '')
  a_stripped = a_stripped.replace('"', '')
  a_stripped = a_stripped.replace(']', '')
  a_split = a_stripped.split(", ")

  print(a_split)
  a_split.remove("regnum")

  print("\nall_deps\n")
  print(a_split)

  cursor.execute("SELECT * FROM departments WHERE regnum = %s", (regnum))

  # s for selected departments
  s_deps = cursor.fetchall()
  s_deps = json.dumps(s_deps, default = str)

  s_stripped = s_deps.strip("[\"]")
  s_stripped = s_stripped.replace('"', '')
  s_split = s_stripped.split(", ")

  print("\nselected_deps\n")
  print(s_split)

  for x in range(len(s_split)): 
    if s_split[x] != '0' :
      print(x)
      index_array.append(x)
  
  # This line is to account for the regnum column in the DB
  index_array = [x - 1 for x in index_array]

  print("\nindex_array\n")
  print(index_array)

  for x in index_array :
    to_return.append(a_split[x])
 
  print("\nto_return\n")
  print(to_return)

  t_return = json.dumps(to_return, default = str)

  return (t_return)


@app.route('/clerk_display', methods=['POST', 'GET'])
def clerk_display():
  print("clerk_display page")

  req_data = request.get_json(force=True)

  regnum = req_data['regnum']

  cursor.execute("SELECT * FROM requests WHERE regnum = %s", (regnum))

  value = cursor.fetchall()
  j_value = json.dumps(value)

  return (j_value)


@app.route('/send_to_dept', methods=['POST', 'GET'])
def send_to_dept():
  print("Sending to specified department")

  req_data = request.get_json(force=True)

  regnum = req_data['regnum']
  single_id = req_data['single_id']
  department = req_data['department']

  print(regnum)
  print(department)

  cursor.execute("UPDATE requests SET process = 'Sent to Dept' WHERE id = %s", (single_id))
  conn.commit()

  cursor.execute("SELECT " + department + " FROM departments WHERE regnum = %s", (regnum))

  email = cursor.fetchone()
  j_email = json.dumps(email)

  print(j_email)

  send_email = j_email.strip("[\"]")

  print(send_email)

  auto_emailer.send_dept_email(send_email)
  # exec(open('auto_emailer.py').read())

  return (j_email)

@app.route('/check_state', methods=['POST', 'GET'])
def check_state():
  print("Checking current state")

  req_data = request.get_json(force=True)

  req_id = req_data['req_id']

  cursor.execute("SELECT process, date_time, email, receipt_sent from requests where id = %s", (req_id))

  state = cursor.fetchall()
  j_state = json.dumps(state)

  return (j_state)


@app.route('/def_email', methods=['POST', 'GET'])
def def_email():
  print("Sending defaulted email")

  req_data = request.get_json(force=True)

  requestor  = req_data['requestor']
  limit_date = req_data['limit_date']

  limit_return_date = limit_date[0:15]

  auto_emailer.send_defaulted_receipt(requestor, limit_return_date)

  return ('xxx', 204)

# Swap state to Request Denied 
# Call python script to send email    
@app.route('/submit_denial', methods=['POST', 'GET'])
def submit_denial():
  print("Submitting denial email")  

  req_data = request.get_json(force=True)

  single_id = req_data['single_id']
  requestor = req_data['requestor']

  cursor.execute("UPDATE requests SET process = 'Denied' WHERE id = %s", (single_id))
  conn.commit()
  
  print("Submitting Denial of Request to " + requestor)

  auto_emailer.send_denial_email(requestor)

  return ('xxx', 204)


@app.route('/furnish_receipt', methods=['POST', 'GET'])
def furnish_receipt():

  req_data = request.get_json(force=True)

  single_id = req_data['single_id']
  requestor = req_data['requestor']

  print("Furnishing receipt to " + requestor)

  cursor.execute("UPDATE requests SET receipt_sent = 1 WHERE id = %s", (single_id))
  conn.commit()

  auto_emailer.send_furnished_receipt(requestor)

  return ('xxx', 204)

if __name__ == '__main__':
	serve(app, listen='*:80')