from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Security and database settings
app.config['SECRET_KEY'] = 'Booba123'
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:root@localhost:5433/flask_gestion"
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
