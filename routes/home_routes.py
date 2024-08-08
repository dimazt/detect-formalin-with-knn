from flask import Blueprint, render_template

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    return render_template('homepage.html', active_page='homepage')

@home_bp.route('/training')
def training_page():
    return render_template('training.html', active_page='training')

@home_bp.route('/testing')
def testing():
    return render_template('testing.html', active_page='testing')
