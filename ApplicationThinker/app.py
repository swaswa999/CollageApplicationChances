#main PYTHON FILE FOR FLASK
import os
from flask import Flask,render_template, redirect, request


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/application')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 81))
    app.run(host=host, port=port, debug=True)
