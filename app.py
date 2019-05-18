from flask import Flask
import os

app = Flask(__name__)
wsgi_app = app.wsgi_app

from modules.routes import *

if __name__ == '__main__':
    """
    Creates a local host server.
    """
    HOST = os.environ.get('SERVER_HOST', "localhost")
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5000
    while True:
        app.run(HOST, PORT)
