from flask import Flask,jsonify,render_template,url_for,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, UniqueConstraint
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'+os.path.join(basedir, 'server.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)

@app.route("/")
def hello():
  return "Hello World!"

if __name__ == "__main__":
  app.run()