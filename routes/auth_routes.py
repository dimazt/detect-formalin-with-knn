from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User
import bcrypt
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))
        user = User.validate_password(email, password)
        print(user)
        if user:
            login_user(user)
            return redirect(url_for('home.index'))
        else:
            flash('Invalid credentials','danger')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    logout_user()
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        user = User.create(fullname,email, password)
        if user:
            flash('User registered successfully', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('User already exists','danger')
    return render_template('signup.html')

@auth_bp.route('/update-password', methods=['POST'])
@login_required
def update_password():
    if request.method == 'POST':
        email = current_user.email
        print(email)
        new_password = request.form['new_password']
        user = User.update_password(email, new_password)
        if user:
            flash('Password updated successfully','success')
        else:
            flash('User does not exist','danger')
    return render_template('update_password.html')

@auth_bp.route('/delete-account/<email>')
@login_required
def delete_account(email):
    if User.delete(email):
        flash('Account deleted successfully','success')
    else:
        flash('User does not exist','danger')
    return redirect(url_for('home.management'))

@auth_bp.route('/dashboard')
@login_required
def dashboard():
    user_role = User.get_role(current_user.id)
    return render_template('dashboard.html', role=user_role)
