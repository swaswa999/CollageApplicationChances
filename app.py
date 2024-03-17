from flask import Flask, redirect, render_template, url_for, request
from openai import OpenAI
from bs4 import BeautifulSoup
from scraper import webscraper
import requests
import os


app = Flask('__main__')

@app.route("/",methods=['GET', 'POST'])
def index():
    isLinksReceived = False
    outputcitations = []
    if request.method == 'POST':
        isLinksReceived = True

        links = request.form.get('link')
        linksArr =  links.splitlines()
        try:
            for i in range(len(linksArr)):
                outputcitations.append(webscraper(linksArr[i]))
        except:
            outputcitations = 'Invalid Link or Links!'



    if isLinksReceived == True:
        return render_template('index.html', outputcitations=outputcitations)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 81))
    app.run(host=host, port=port, debug=True)