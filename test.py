# -*-:coding:utf-8 -*-

import os,unittest
from config import basedir
from app import app,db
from app.models import User

#unit test
class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING']=True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_avatar(self):
        u=User(nickname='斌',email='caibird1985@yahoo.com')
        avatar=u.avatar(128)
        expected='http://www.gravatar.com/avatar/56b2d80c1a66347aba3d5f2f1d5e682b?d=mm&s=128'
        assert avatar[0:len(expected)]==expected

    def test_make_unique_nickname(self):
        u = User(nickname='斌', email='caibird1985@yahoo.com')
        db.session.add(u)
        db.session.commit()
        nickname = User.make_unique_nickname('斌')
        assert nickname != '斌'
        u = User(nickname=nickname, email='susan@example.com')
        db.session.add(u)
        db.session.commit()
        nickname2 = User.make_unique_nickname('斌')
        assert nickname2 != '斌'
        assert nickname2 != nickname

if __name__=='__main__':
    unittest.main()
