from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] =  'postgres://uoiylklneqfjqg:S06nT_ubANrMtmL5tAufL2NjQ7@ec2-54-83-3-38.compute-1.amazonaws.com:5432/debueie1m71hib'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://project3180:project3180@localhost/project3180"
db=SQLAlchemy(app)
db.create_all()

from app import views, models
 