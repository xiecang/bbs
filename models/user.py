import hashlib
from flask import current_app
from flask_login import LoginManager
from flask_login import UserMixin
from flask_login import AnonymousUserMixin
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from models import db
from models import ModelMixin
from models.role import Role
from models.role import Permission
from utils import timestamp


class User(db.Model, ModelMixin, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(db.Integer)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    introduction = db.Column(db.String(128))
    avatar = db.Column(db.String(128))
    topics = db.relationship('Topic', backref='user')
    comments = db.relationship('Comment', backref='user')
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError(u'密码不可读')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @classmethod
    def validate(cls, form):
        username = form.get('username', '')
        password = form.get('password', '')
        user = User.query.filter_by(username=username).first()
        if user is not None and check_password_hash(user.password_hash, password):
            return user
        else:
            return None

    def validate_register(self):
        if len(self.username) > 0:
            return True
        else:
            return False

    def change_password(self, form):
        password = form.get('password', '')
        password_new = form.get('password_new', '')
        password_new_repeat = form.get('password_new_repeat', '')
        r = {
            'setting_ok': False,
        }
        if check_password_hash(self.password_hash, password):
            if password_new == password_new_repeat:
                self.password = password_new
                self.save()
                r['setting_ok'] = True
            else:
                r['error_message'] = u'新密码两次输入不一致'
        else:
            r['error_message'] = u'当前密码错误'
        return r

    def gravatar(self, size=100, default='identicon', rating='g'):
        if self.avatar is not None:
            return self.avatar
        else:
            url = 'http://cn.gravatar.com/avatar'
            hash = hashlib.md5(self.username.encode('utf-8')).hexdigest()
            s = '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
                url=url,
                hash=hash,
                size=size,
                default=default,
                rating=rating
            )
            return s

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def __init__(self, form):
        self.created_time = timestamp()
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        role = None
        if self.username == current_app.config['ADMIN']:
            role = Role.query.filter_by(name='Administrator').first()
            print('admin role', role)
        else:
            role = Role.query.filter_by(name='User').first()
            print('role', role)
        self.role_id = role.id


class AnonymousUser(AnonymousUserMixin):
    def can(slef, permissions):
        return False

    def is_administrator(self):
        return False


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login_view'
login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
