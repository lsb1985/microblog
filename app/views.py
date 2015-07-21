# -*-coding:utf-8 -*-

__author__='caibird'

'''
views
'''

from app import app
from flask import render_template,flash,redirect
from .forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
	user={'nickname':'caibird'}

	posts=[
	{
		'author':{'nickname':'caibird'},
		'body':'Beautiful day in Portland!'
	},
	{
		'author':{'nickname':'zero'},
		'body':'The Avengers movie was so cool!'
	}

	]

	return render_template("index.html",posts=posts,user=user)

@app.route('/login',methods=['POST','GET'])
def login():
	form=LoginForm()
	if form.validate_on_submit():
		flash('Login requested for OpenID="'+form.openid.data+'",remember_me='+str(form.remember_me.data))
		return redirect('/index')
	return render_template('login.html',title='Sign In',form=form,providers=app.config['OPENID_PROVIDERS'])