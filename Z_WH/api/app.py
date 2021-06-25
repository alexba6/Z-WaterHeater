from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

app.config['debug'] = True
app.config['CORS_HEADERS'] = True

CORS(app)
