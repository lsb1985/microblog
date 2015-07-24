# -*-coding:utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir
import os


app=Flask(__name__)
app.config.from_object('config')
db=SQLAlchemy(app)

lm=LoginManager()
lm.init_app(app)
oid=OpenID(app,os.path.join(basedir,'tmp'))
lm.login_view='login' #让Flask-Login 知道哪个视图允许用户登录

from app import views,models

