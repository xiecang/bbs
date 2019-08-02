from models import db
from models import ModelMixin
from models.node import Node
from utils import timestamp


class Topic(db.Model, ModelMixin):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(db.Integer)
    title = db.Column(db.String(64))
    content = db.Column(db.Text())
    clicked = db.Column(db.Integer)
    visit_count = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='topic', lazy="dynamic")
    top_node_id = db.Column(db.Integer, db.ForeignKey('top_nodes.id'))
    node_id = db.Column(db.Integer, db.ForeignKey('nodes.id'))

    def __init__(self, form):
        self.created_time = timestamp()
        self.clicked = 0
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.node_id = int(form.get('node', '0'))
        node = Node.query.filter_by(id=self.node_id).first()
        self.top_node_id = node.top_node_id

    def validate(self):
        if len(self.title) > 0:
            return True
        else:
            return False
