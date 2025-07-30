
import requests
from dotenv import load_dotenv
import os
from flask import Flask#importing flask

load_dotenv()
api_key = os.getenv("API_KEY") #Environment setup should happen before you define routes(web app instance)

app = Flask (__name__)# this creates the web app instance. __name__ refers to the current Python module
@app.route('/')


def hello():
    return 'Hello from Flask'

if __name__ =="__main__": #to run the app
    app.run()