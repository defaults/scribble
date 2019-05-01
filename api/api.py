from flask import Blueprint, request, jsonify, session, render_template
from flask_login import login_required

api = Blueprint('api', 'api', url_prefix='/api')


@api.route('/articles', methods=['GET'])
def get_all_articles():
    pass


@api.route('/article', methods=['POST'])
def create_article():
    pass


@api.route('/article/<string:article_name>', methods=['GET', 'PUT', 'DELETE'])
def article(article_name):
    pass


@login_required
@api.route('/subscribers', methods=['GET'])
def get_subscribers():
    pass


@api.route('/subscriber>', methods=['POST'])
def add_subscriber():
    pass


@api.route('/subscriber/<uuid:id>', methods=['DELETE'])
def delete_subscriber(id):
    pass


@login_required
@api.route('/tags', methods=['GET'])
def get_tags():
    pass


@login_required
@api.route('/tag', methods=['POST'])
def add_tag():
    pass


@api.route('/tag/<uuid:id>', methods=['DELETE'])
def delete_tag(id):
    pass


@api.route('/short_url', methods=['POST'])
def create_short_url():
    pass


@login_required
@api.route('/config', methods=['GET', 'POST', 'PATCH'])
def config():
    pass
