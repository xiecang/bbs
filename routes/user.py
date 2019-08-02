import os
from werkzeug import secure_filename
from flask import current_app
from routes import *
from routes.auth import login_required
from routes.auth import current_user
from utils import log


main = Blueprint('user', __name__)


def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    allow = '.' in filename and filename.rsplit('.', 1)[1] in allowed_extensions
    return allow


@main.route('/')
@login_required
def index():
    return redirect(url_for('user.settings'))


@main.route('/settings')
@login_required
def settings():
    user = current_user._get_current_object()
    return render_template('user/setting.html', user=user)


@main.route('/settings/avatar')
@login_required
def settings_avatar():
    user = current_user._get_current_object()
    return render_template('user/avatar_upload.html', user=user)


@main.route('/avatar_upload', methods=['POST'])
@login_required
def avatar_upload():
    file = request.files['file']
    if file and allowed_file(file.filename):
        user = current_user._get_current_object()
        extension = secure_filename(file.filename).split('.')[-1]
        filename = '{}_avatar.{}'.format(user.username, extension)
        log('filename', filename)
        file.save(os.path.join(current_app.config['AVATAR_FOLDER'], filename))
        user.avatar = url_for('user.avatar', avatar_name=filename)
        # log('user.avatar,', user.avatar)
        user.save()
        flash(u'头像上传成功')
    return redirect(url_for('user.settings_avatar'))


@main.route('/avatar/<avatar_name>')
def avatar(avatar_name):
    return send_from_directory(current_app.config['AVATAR_FOLDER'], avatar_name)


@main.route('/change_password', methods=['POST'])
@login_required
def change_password():
    form = request.form
    user = current_user._get_current_object()
    r = user.change_password(form)
    if r['setting_ok']:
        flash(u'密码更改成功')
        return redirect(url_for('auth.logout'))
    flash(r['error_message'])
    return redirect(url_for('user.index'))
