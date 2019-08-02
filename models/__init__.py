import time
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class ModelMixin(object):
    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{0} = {1}'.format(k, v) for k, v in self.__dict__.items())
        return '<{0}: \n  {1}\n>'.format(class_name, '\n  '.join(properties))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_created_time(self):
        value = time.localtime(self.created_time)
        y = time.strftime('%Y', value)
        m = time.strftime('%m', value)
        d = time.strftime('%d', value)
        t = time.strftime('%H:%M:%S', value)
        dt = '{}/{}/{} {}'.format(y, m, d, t)
        return dt
