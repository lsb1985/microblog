# -*-coding:utf-8 -*-

__author__='caibird'

'''
forms
'''

from flask.ext.wtf import Form
from wtforms import StringField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length

#login form
class LoginForm(Form):
	openid=StringField('openid',validators=[DataRequired()])
	remember_me=BooleanField('remember_me',default=False)
		
#edit user info
class EditForm(Form):
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])