from flask import Flask
from flask_bootstrap import Bootstrap
import sqlite3


app = Flask(__name__)
Bootstrap(app)
app.config.from_object('config')

from app import views
