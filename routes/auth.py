from functools import wraps
from models.role import Permission
from models.user import User
from routes import *
from utils import log


main = Blueprint('auth', __name__)


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return function
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)


@main.route('/')
def index():
    return redirect(url_for('.login_view'))


@main.route('/login')
def login_view():
    flash(u'你要查看的页面需要先登录')
    return render_template('auth/login.html')


@main.route('/register')
def register_view():
    return render_template('auth/register.html')


@main.route('/login', methods=['POST'])
def login():
    form = request.form
    u = User.validate(form)
    if u is not None:
        login_user(u)
        log('登录成功')
        return redirect(url_for('topic.index'))
    else:
        log('登录失败')
        flash(u'用户名或密码错误')
    return redirect(url_for('auth.login_view'))


@main.route('/register', methods=['POST'])
def register():
    form = request.form
    u = User(form)
    user = User.query.filter_by(username=u.username).first()
    if user is None and u.validate_register():
        log('注册成功')
        u.save()
        return redirect(url_for('auth.login_view'))
    else:
        log('注册失败')
        if user is not None:
            flash(u'注册失败，用户名已注册')
        else:
            flash(u'注册失败，用户名或密码不能为空')
    return redirect(url_for('auth.register_view'))


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login_view'))
