from flask import Flask
from sense_hat import SenseHat
import signal
import sys

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()