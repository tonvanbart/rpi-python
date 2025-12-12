from flask import Flask
from sense_hat import SenseHat
import signal
import sys

app = Flask(__name__)
sense = SenseHat()
sense.set_rotation(180)
count = 0

@app.route('/')
def hello_world():
    # show something on the hat when the server is hit
    global count
    count = count + 1
    sense.show_message('hit ' + str(count))
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0') # make server visible on local network