from flask import Flask
from flask_migrate import Migrate
from flask_migrate import MigrateCommand
from flask_script import Manager
from flask_script import Shell
from models import db
from models.user import User
from models.user import login_manager
from models.role import Role
from routes.topic import main as routes_topic
from routes.auth import main as routes_auth
from routes.user import main as routes_user
from routes.manage import main as routes_manage
from settings import app_config


app = Flask(__name__)
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


def register_routes(app):
    app.register_blueprint(routes_topic)
    app.register_blueprint(routes_auth, url_prefix='/auth')
    app.register_blueprint(routes_user, url_prefix='/user')
    app.register_blueprint(routes_manage, url_prefix='/manage')


def configure_app():
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.secret_key = app_config['secret_key']
    app.config['SQLALCHEMY_DATABASE_URI'] = app_config['database_url']
    app.config['AVATAR_FOLDER'] = 'static/img/user_avatar'
    app.config['ADMIN'] = app_config['admin']
    db.init_app(app)
    # 创建所有表
    with app.app_context():
        db.create_all()
    register_routes(app)
    login_manager.init_app(app)


def configured_app():
    configure_app()
    return app


# 自定义的命令行命令用来运行服务器
@manager.command
def run():
    config = dict(
        debug=True,
        host='127.0.0.1',
        port=5000,
    )
    app.run(**config)


def configure_manager():
    """
    这个函数用来配置命令行选项
    """
    Migrate(app, db)
    manager.add_command('db', MigrateCommand)
    manager.add_command('shell', Shell(make_context=make_shell_context))


def local_run():
    config = dict(
        debug=True,
        host='127.0.0.1',
        port=5000,
    )
    import os

    d = "ignoreme/profile"
    if not os.path.exists(d):
        os.mkdir(d)

    from werkzeug.middleware.profiler import ProfilerMiddleware

    null = open(os.devnull, "w")
    app.wsgi_app = ProfilerMiddleware(
        app.wsgi_app,
        stream=null,
        profile_dir=d,
        filename_format="{time}.{method}.{path}.{elapsed:06f}ms.prof", )
    print(app.url_map)

    app.run(**config)


if __name__ == '__main__':
    configure_manager()
    configure_app()
    local_run()
