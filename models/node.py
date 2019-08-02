from models import db
from models import ModelMixin
from utils import timestamp

import hashlib


class TopNode(db.Model, ModelMixin):
    __tablename__ = 'top_nodes'
    id = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(db.Integer)
    name = db.Column(db.String(64))
    introduction = db.Column(db.String(128))
    nodes = db.relationship('Node', backref='top_node', lazy='dynamic')
    topics = db.relationship('Topic', backref="top_node", lazy="dynamic")

    def __init__(self, form):
        self.created_time = timestamp()
        self.name = form.get('top_node_name', '')
        self.introduction = form.get('top_node_inctoduction', '')

    def validate(self):
        return True


class Node(db.Model, ModelMixin):
    __tablename__ = 'nodes'
    id = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(db.Integer)
    name = db.Column(db.String(64))
    introduction = db.Column(db.String(128))
    top_node_id = db.Column(db.Integer, db.ForeignKey('top_nodes.id'))
    topics = db.relationship('Topic', backref="node", lazy="dynamic")

    def __init__(self, form):
        self.created_time = timestamp()
        self.top_node_id = int(form.get('top_node', '0'))
        self.name = form.get('node_name', '')
        self.introduction = form.get('node_inctoduction', '')

    def validate(self):
        return True

    def gravatar(self, size=100, default='identicon', rating='g'):
        url = 'http://cn.gravatar.com/avatar'
        hash = hashlib.md5(self.name.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url = url, hash = hash, size = size, default = default, rating = rating)
