from models.topic import Topic
from models.comment import Comment
from models.user import User
from models.node import TopNode
from models.node import Node
from routes import *
from routes.auth import login_required
from routes.auth import current_user
from utils import log
import time


main = Blueprint('topic', __name__)

Model = Topic


@main.route('/')
def index():
    top_node = TopNode.query.first()
    if top_node is not None:
        id = top_node.id
        return redirect(url_for('topic.tab', id=id))
    return redirect(url_for('topic.all'))


@main.route('/tab/<int:id>')
def tab(id):
    all_list = {
        'top_node_list': TopNode.query.all(),
    }
    statistics = {
        'user': User.query.count(),
        'topic': Topic.query.count(),
        'comment': Comment.query.count()
    }
    top_node = TopNode.query.filter_by(id=id).first()
    if top_node is not None:
        all_list['topic_list'] = Topic.query.filter_by(top_node_id=top_node.id).order_by(Topic.created_time.desc()).all()
        all_list['node_list'] = top_node.nodes
    else:
        all_list['topic_list'] = []
        all_list['node_list'] = []
    return render_template('topic_index.html', top_node_id=id, all_list=all_list, statistics=statistics)


@main.route('/topic/all')
def all():
    all_list = {
        'top_node_list': TopNode.query.all(),
        'node_list': Node.query.all(),
        'topic_list': Topic.query.order_by(Topic.created_time.desc()).all()
    }
    statistics = {
        'user': User.query.count(),
        'topic': Topic.query.count(),
        'comment': Comment.query.count()
    }
    return render_template('topic_all.html', all_list=all_list, statistics=statistics)


@main.route('/t/<int:id>')
def topic(id):
    topic = Model.query.get(id)
    if topic is not None:
        topic.clicked += 1
        topic.save()
        return render_template('topic.html', topic=topic)
    return redirect(url_for('topic.index'))


@main.route('/add')
def add_view():
    node_list = Node.query.all()
    return render_template('topic_add.html', node_list=node_list)


@main.route('/add', methods=['POST'])
@login_required
def add():
    form = request.form
    t = Topic(form)
    if t.validate():
        t.user = current_user._get_current_object()
        t.save()
        flash(u'发布成功')
        return redirect(url_for('topic.topic', id=t.id))
    else:
        flash(u'标题不能为空')
    return redirect(url_for('topic.add_view'))


@main.route('/add/from/node', methods=['POST'])
@login_required
def add_from_node():
    form = request.form
    t = Topic(form)
    if t.validate():
        t.user = current_user._get_current_object()
        t.save()
        flash(u'创建新主题成功')
        return redirect(url_for('topic.node', id=t.node.id))
    return redirect(url_for('topic.index'))


@main.route('/edit/<int:id>')
@login_required
def edit_view(id):
    topic = Model.query.get(id)
    if topic is not None and (current_user == topic.user or current_user.is_administrator()):
        node_list = Node.query.all()
        return render_template('topic_edit.html', topic=topic, node_list=node_list)
    return redirect(url_for('topic.topic', id=id))


@main.route('/edit/<int:id>', methods=['POST'])
@login_required
def edit(id):
    form = request.form
    t = Topic(form)
    topic = Model.query.get(id)
    if topic is not None and t.validate() and (current_user == topic.user or current_user.is_administrator()):
        topic.title = t.title
        topic.content = t.content
        topic.node_id = t.node_id
        topic.save()
        flash(u'更改成功')
        return redirect(url_for('topic.topic', id=id))
    else:
        flash(u'标题不能为空')
    return redirect(url_for('topic.edit_view', id=id))


@main.route('/delete/<int:id>')
@login_required
def delete(id):
    topic = Model.query.get(id)
    if topic is not None and (current_user == topic.user or current_user.is_administrator()):
        for c in topic.comments:
            c.delete()
        topic.delete()
        return redirect(url_for('topic.index'))
    return redirect(url_for('topic.topic', id=id))


@main.route('/comment', methods=['POST'])
@login_required
def comment():
    form = request.form
    c = Comment(form)
    log('topic id', c.topic_id)
    log('comment', c.content)
    if c.validate():
        user = current_user._get_current_object()
        timestamp = int(time.time())
        last_comment = Comment.query.filter_by(user_id=user.id).order_by(Comment.created_time.desc()).first()
        if last_comment is None:
            c.user = user
            c.save()
        elif timestamp - last_comment.created_time > 2:
            c.user = user
            c.save()
        else:
            flash(u'2 秒之内只能回复一次')
    else:
        flash(u'回复内容不能为空')

    return redirect(url_for('topic.topic', id=c.topic_id))


@main.route('/comment/delete/<int:id>')
@login_required
def comment_delete(id):
    c = Comment.query.get(id)
    if c is not None and (current_user == c.user or current_user.is_administrator()):
        c.delete()
    return redirect(url_for('topic.topic', id=c.topic_id))


@main.route('/node/<int:id>')
def node(id):
    n = Node.query.get(id)
    if n is not None:
        topic_list = Topic.query.filter_by(node_id=n.id).order_by(Topic.created_time.desc()).all()
        return render_template('node.html', n=n, topic_list=topic_list)
    return redirect(url_for('topic.index'))
