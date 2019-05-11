from flask import Flask
import os

app = Flask(__name__)
wsgi_app = app.wsgi_app

from routes import *

if __name__ == '__main__':
    HOST = os.environ.get('SERVER_HOST', "localhost")
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5000
    app.run(HOST, PORT)
