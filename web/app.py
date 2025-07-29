#importing flask
from flask import Flask
app = Flask (__name__)# create an instance of app and stores in app variable. __name__ refers to the current Python module

@app.route('/')
def hello():
    return 'Hello from Flask'

if __name__ =="__main__":
    app.run()