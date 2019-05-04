from flask import Blueprint, request, jsonify, session, render_template
from flask_login import login_required

admin = Blueprint('admin', 'admin', url_prefix='/a')


@login_required
@admin.route('/welcome', methods=['GET'])
def admin_onboarding():
    pass


@login_required
@admin.route('/dashboard', methods=['GET'])
def dashboard():
    pass


@login_required
@admin.route('/account', methods=['GET'])
def account():
    pass
