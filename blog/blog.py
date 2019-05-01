from flask import Blueprint, request, jsonify, session, render_template

blog = Blueprint('blog', 'blog')


@blog.route('/<string:article_name>', methods=['GET'])
def article():
    pass


@blog.route('/', methods=['GET'])
def articles():
    pass
