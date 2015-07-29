# -*-coding:utf-8 -*-

import os


#CSRF_ENABLED 配置是为了激活 跨站点请求伪造 保护
CSRF_ENABLED=True
#当 CSRF 激活的时候才需要，它是用来建立一个加密的令牌，用于验证一个表单
SECRET_KEY='you-will-never-guess'

# OpenID 提供者的列表
OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://accounts.google.com/ServiceLogin'},
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]

basedir=os.path.abspath(os.path.dirname(__file__))

#Flask-SQLAlchemy 扩展需要,这是我们数据库文件的路径
SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(basedir,'app.db')
#文件夹，我们将会把 SQLAlchemy-migrate 数据文件存储在这里
SQLALCHEMY_MIGRATE_REPO=os.path.join(basedir,'db_repository')


#mail setting
#在本地伪造一个邮件服务器  python -m smtpd -n -c DebuggingServer localhost:25
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None

#administrator list
ADMINS=['466255983@qq.com']
