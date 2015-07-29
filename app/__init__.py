# -*-coding:utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir,ADMINS,MAIL_SERVER,MAIL_PORT,MAIL_USERNAME,MAIL_PASSWORD
import os


app=Flask(__name__)
app.config.from_object('config')
db=SQLAlchemy(app)

lm=LoginManager()
lm.init_app(app)
oid=OpenID(app,os.path.join(basedir,'tmp'))
lm.login_view='login' #让Flask-Login 知道哪个视图允许用户登录

if not app.debug:
	import logging

	#发送邮件告警
	from logging.handlers import SMTPHandler
	credentials=None
	if MAIL_USERNAME or MAIL_PASSWORD:
		credentials=(MAIL_USERNAME,MAIL_PASSWORD)
	mail_handler=SMTPHandler((MAIL_SERVER,MAIL_PORT),'no-reply@'+MAIL_SERVER,ADMINS,'microblog failure',credentials)
	mail_handler.setLevel(logging.ERROR)
	app.logger.addHandler(mail_handler)

	#打印日志在tmp目录
	from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('microblog startup')

from app import views,models

 