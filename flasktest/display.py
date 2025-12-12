from flask import Flask, render_template, redirect, url_for, request
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
    return render_template('display.html', count=count)

@app.route('/message', methods=['POST'])
def show_message():
    message = request.form['message']
    sense.show_message(message)
    return redirect(url_for('hello_world'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True) # make server visible on local network