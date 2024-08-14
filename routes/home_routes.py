from flask import Blueprint, jsonify, render_template
from flask_login import login_required, current_user
from models.user import User, admin_permission
from models.knn import read_n_neighbors
home_bp = Blueprint('home', __name__)

@home_bp.route('/')
@login_required
def index():
    return render_template('homepage.html', active_page='homepage')

@home_bp.route('/training')
@login_required
def training_page():
    return render_template('training.html', active_page='training')

@home_bp.route('/testing')
@login_required
def testing():
    knn = read_n_neighbors()
    return render_template('testing.html', active_page='testing', k_value = knn)

@home_bp.route('/management-user')
@login_required
def management():
    users = User.load_users()
    return render_template('management_user.html', active_page='management', users=users)

@home_bp.route('/setting')
@login_required
def setting():
    return render_template('update_password.html', active_page='setting')

@home_bp.route('/is-login', methods=['GET'])
def is_login():
    if current_user.is_authenticated:
        # Extract the actual user data you want to return
        user_data = {
            'id': current_user.id,
            'email': current_user.email,
            'fullname': current_user.fullname,
            'role': current_user.role
        }
        return jsonify({'isLogin': True, 'user': user_data})
    else:
        return jsonify({'isLogin': False})
