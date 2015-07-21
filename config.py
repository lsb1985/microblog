#CSRF_ENABLED 配置是为了激活 跨站点请求伪造 保护
CSRF_ENABLED=True
#当 CSRF 激活的时候才需要，它是用来建立一个加密的令牌，用于验证一个表单
SECRET_KEY='you-will-never-guess'

# OpenID 提供者的列表
OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]