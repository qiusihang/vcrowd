from flask import Flask, render_template, request, jsonify
from instance import *

app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/jquery.min.js')
def jquery():
    return render_template('jquery.min.js')

@app.route('/cssim.js')
def cssim():
    return render_template('cssim.js')

@app.route('/addnumber')
def add():
    a = request.args.get('a', 0, type=float)
    b = request.args.get('b', 0, type=float)
    return jsonify(result=a + b)

@app.route('/run')
def run():
    i = Instance()
    i.run()

if __name__ == '__main__':
    app.run()
