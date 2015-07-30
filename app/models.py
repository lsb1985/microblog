# -*-coding:utf-8 -*-

from app import db
import hashlib

#关注，关联表
followers=db.Table('followers',
    db.Column('follower_id',db.Integer,db.ForeignKey('user.id')),
    db.Column('followed_id',db.Integer,db.ForeignKey('user.id')))


#User table
class User(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	nickname=db.Column(db.String(64),index=True,unique=True)
	email = db.Column(db.String(120), index = True, unique = True)
	posts=db.relationship('Post',backref='author',lazy='dynamic') #对于一个一对多的关系，db.relationship 字段通常是定义在“一”这一边
	about_me = db.Column(db.String(140))
	last_seen = db.Column(db.DateTime)
	followed=db.relationship('User',secondary=followers,primaryjoin=(followers.c.follower_id==id),secondaryjoin=(followers.c.followed_id==id),backref=db.backref('followers',lazy='dynamic'),lazy='dynamic')

	def avatar(self,size):
		return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' %(hashlib.md5(self.email.encode('utf-8')).hexdigest(),size)

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

    def is_following(self,user):
        return self.followed.filter_by(followers.c.followed_id==user.id).count()>0

    #成功返回一个对象，失败返回None
    def follow(self,user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    #成功返回一个对象，失败返回None
    def unfollow(self,user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    #查询关注者blog的索引
    def followed_posts(self):
        return Post.query.join(followers,(followers.c.followed_id==Post.user_id)).filter(followers.c.follower_id==self.id).order_by(Post.timestamp.desc())

	@staticmethod
	def make_unique_nickname(nickname):
	    if User.query.filter_by(nickname = nickname).first() == None:
	        return nickname
	    version = 2
	    while True:
	        new_nickname = nickname + str(version)
	        if User.query.filter_by(nickname = new_nickname).first() == None:
	            break
	        version += 1
	    return new_nickname

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