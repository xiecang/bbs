from models import db
from models import ModelMixin
from utils import timestamp


class Comment(db.Model, ModelMixin):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(db.Integer)
    content = db.Column(db.Text())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))

    def __init__(self, form):
        self.created_time = timestamp()
        self.topic_id = form.get('topic_id', '')
        self.content = form.get('comment', '')

    def validate(self):
        if len(self.content) > 0:
            return True
        else:
            return False
