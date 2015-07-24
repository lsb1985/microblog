# -*-coding:utf-8 -*-

from app import db

#User table
class User(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	nickname=db.Column(db.String(64),index=True,unique=True)
	email = db.Column(db.String(120), index = True, unique = True)
	posts=db.relationship('Post',backref='author',lazy='dynamic') #对于一个一对多的关系，db.relationship 字段通常是定义在“一”这一边

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return True

	def get_id(self):
		try:
			return unicode(self.id) # python 2
		except NameError:
			return str(self.id) # python 3

	#告诉Python如何打印这个类的对象,我们将用它来调试
	def __repr__(self):
		return '<User %r>' %(self.nickname)

	
#Post table	
class Post(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	body = db.Column(db.String(140))
	timestamp=db.Column(db.DateTime)
	user_id=db.Column(db.Integer,db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Post %r>' %(self.body)