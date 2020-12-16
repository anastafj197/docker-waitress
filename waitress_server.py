# Author    : Frances Anastasia 
# Developed : 12/16/2020

# Waitress Server : A production WSGI server

#import foil_server
import flask_app.py

from waitress import serve 

#serve(foil_server.app, host='192.168.1.196', port=5000, url_scheme='https')
serve(flask_app.app, host='0.0.0.0', port=5000)