from flask import Flask
from asyncwsgi.server import run

app = Flask(__name__)

@app.route('/')
def index():
	return "Hello World!"


run(app)