# -*-coding:utf-8 -*-

__author__='caibird'

'''
views
'''

from app import app,db,lm,oid
from flask import render_template,flash,redirect,session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from .forms import LoginForm
from .models import User

@app.route('/')
@app.route('/index')
@login_required
def index():
	user=g.user

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

	return render_template("index.html",title='Home',posts=posts,user=user)

@app.route('/login',methods=['POST','GET'])
@oid.loginhandler
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	form = LoginForm()
	#如果 validate_on_submit 在表单提交请求中被调用，它将会收集所有的数据，对字段进行验证，如果所有的事情都通过的话，它将会返回 True，表示数据都是合法的。这就是说明数据是安全的，并且被应用程序给接受了
	if form.validate_on_submit():
		session['remember_me']=form.remember_me.data
		return oid.try_login(form.openid.data,ask_for=['nickname','email']) #触发FLASK-openid认证
		#flash('Login requested for OpenID="'+form.openid.data+'",remember_me='+str(form.remember_me.data))
	print('aaa')
	return render_template('login.html',title='Sign In',form=form,providers=app.config['OPENID_PROVIDERS'])



#openid认证后返回的oid.after_login,检查openid是否正确
@oid.after_login
def after_login(resp):
	if resp.email is None or resp.email=="":
		flash('Invalid login.Please try again.')
		return redirect(url_for('index'))
	
	user=User.query.filter_by(email=resp.email).first()
	if user is None:
		nickname=resp.nickname
		if nickname is None or nickname=="":
			nickname=resp.email.split('@')[0]
		user=User(nickname=nickname,email=resp.email)
		db.session.add(user)
		db.session.commit()
	remember_me=False
	if 'remember_me' in session:
		remember_me=session['remember_me']
		session.pop('remember_me',None)
	login_user(user,remember=remember_me)
	return redirect(request.args.get('next') or url_for('index'))

#注销
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

#检查g.user是否是已登录用户
@app.before_request
def before_request():
	g.user=current_user

#回掉，返回用户
@lm.user_loader
def load_user(id):
	return User.query.get(int(id))