from flask import Flask, send_from_directory
from flask_login import LoginManager
from config import Config
from models.user import User
from routes.home_routes import home_bp
from routes.knn_routes import knn_bp
from routes.auth_routes import auth_bp
from flask_principal import Principal
app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = 'secretBanget'

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
principal = Principal(app)
@login_manager.user_loader
def load_user(user_id):
    users = User.load_users()
    for user_data in users:
        if user_data['id'] == int(user_id):
            return User(
                id=user_data['id'],
                fullname=user_data.get('fullname', user_data['email']),  # Default to email if fullname is not provided
                email=user_data['email'],
                password=user_data['password'],
                role=user_data.get('role', 'user')  # Default to 'user' role
            )
    return None


    # Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)
app.register_blueprint(knn_bp)

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
