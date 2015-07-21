# -*-coding:utf-8 -*-

__author__='caibird'

'''
forms
'''

from flask.ext.wtf import Form
from wtforms import StringField,BooleanField
from wtforms.validators import DataRequired

#login form
class LoginForm(Form):
	openid=StringField('openid',validators=[DataRequired()])
	remember_me=BooleanField('remember_me',default=False)
		