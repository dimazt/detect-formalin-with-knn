from flask import Flask, send_from_directory
from config import Config
from routes.home_routes import home_bp
from routes.knn_routes import knn_bp

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(home_bp)
app.register_blueprint(knn_bp)

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
