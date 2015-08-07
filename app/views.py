# -*-coding:utf-8 -*-

__author__='caibird'

'''
views
'''

from app import app,db,lm,oid
from flask import render_template,flash,redirect,session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from .forms import LoginForm,EditForm,PostForm,SearchForm
from .models import User,Post
from datetime import datetime
from config import POSTS_PER_PAGE,MAX_SEARCH_RESULTS


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/', methods=['GET', 'POST'])
@app.route('/index/<int:page>',methods=['GET','POST'])
@login_required
def index(page=1):
	# user=g.user
	form=PostForm()
	if form.validate_on_submit():
		post=Post(body=form.post.data,timestamp=datetime.utcnow(),author=g.user)
		db.session.add(post)
		db.session.commit()
		flash('Your post is now live!')
		return redirect(url_for('index'))
		# return redirect(url_for('index'))

	posts = g.user.followed_posts().paginate(page, POSTS_PER_PAGE, False)
	return render_template("index.html",title='Home',posts=posts,form=form)

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
		#make the user follow him/herself
		db.session.add(user.follow(user))
		db.session.commit()

	remember_me=False
	if 'remember_me' in session:
		remember_me=session['remember_me']
		session.pop('remember_me',None)
	login_user(user,remember=remember_me)
	return redirect(request.args.get('next') or url_for('index'))


#用户视图
@app.route('/user/<nickname>')
@app.route('/user/<nickname>/<int:page>')
@login_required
def user(nickname,page=1):
    user=User.query.filter_by(nickname=nickname).first()
    if user is None:
        nickname=resp.nickname
        if nickname is None or nickname=="":
            nickname=resp.nickname.split('@')[0]
        nickname=User.make_unique_nickname(nickname)
        user=User(nickname=nickname,email=resp.email)
        db.session.add(user)
        db.session.commit()
		#flash('User'+nickname+'is not found.')
		#return redirect(url_for('index'))
    posts=user.posts.paginate(page,POSTS_PER_PAGE,False)
    return render_template('user.html',user=user,posts=posts)

#编辑用户信息
@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form=form)

#关注
@app.route('/follow/<nickname>')
@login_required
def follow(nickname):
    user=User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s is not found.' %nickname)
        return redirect(url_for('index'))
    #不能关注自己？
    if user==g.user:
        flash('You can\'t follow yourself!')
        return redirect(url_for('user',nickname=nickname))
    u=g.user.follow(user)
    if u is None:
        flash('Cannot follow ' + nickname + '.')
        return redirect(url_for('user',nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You are following ' +nickname+'!')
    return redirect(url_for('user',nickname=nickname))

#取消关注
@app.route('/unfollow/<nickname>')
@login_required
def unfollow(nickname):
    user=User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s is not found.' %nickname)
        return redirect(url_for('index'))
    if user==g.user:
        flash('You can\'t unfollow yourself!')
        return redirect(url_for('user',nickname=nickname))
    u=g.user.unfollow()
    if u is None:
        flash('Cannot unfollow ' + nickname + '.')
        return redirect(url_for('user',nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You are stopped following ' +nickname+'!')
    return redirect(url_for('user',nickname=nickname))

#搜索视图
@app.route('/search', methods = ['POST'])
@login_required
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('index'))
    return redirect(url_for('search_results', query = g.search_form.search.data))

@app.route('/search_results/<query>')
@login_required
def search_results(query):
	results = Post.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
	print("results:%s"%results)
	return render_template('search_results.html',query = query,results = results)  

#注销
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

#检查g.user是否是已登录用户
@app.before_request
def before_request():
	g.user=current_user
	if g.user.is_authenticated():
		g.user.last_seen=datetime.utcnow()
		db.session.add(g.user)
		db.session.commit()
		g.search_form=SearchForm() #搜索表单对所有模板生效

#回掉，返回用户
@lm.user_loader
def load_user(id):
	return User.query.get(int(id))


#404错误
@app.errorhandler(404)
def internal_error(error):
	return render_template('404.html'),404

#500错误
@app.errorhandler(500)
def internal_error(error):
	db.session.rollback() #roll back database
	return render_template('500.html'),500

