from models.node import TopNode
from models.node import Node
from routes import *
from routes.auth import login_required
from routes.auth import admin_required


main = Blueprint('manage', __name__)


@main.route('/')
@login_required
@admin_required
def index():
    top_node_list = TopNode.query.all()
    node_list = Node.query.all()
    return render_template('manage/index.html', top_node_list=top_node_list, node_list=node_list)


@main.route('/top_node_add', methods=['POST'])
@login_required
@admin_required
def top_node_add():
    form = request.form
    top_node = TopNode(form)
    if top_node.validate():
        top_node.save()
    return redirect(url_for('manage.index'))


@main.route('/node_add', methods=['POST'])
@login_required
@admin_required
def node_add():
    form = request.form
    node = Node(form)
    if node.validate():
        node.save()
    return redirect(url_for('manage.index'))
