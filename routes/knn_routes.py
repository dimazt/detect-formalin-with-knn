import os
import threading
from flask import Blueprint, request, jsonify, url_for, current_app
from utils.image_processing import allowed_file, process_image, extract_rgb, rgb_to_hsv
from utils.knn_model import train_model, identify_image
from werkzeug.utils import secure_filename
import uuid
from flask_login import current_user
from models.knn import create_n_neighbors,read_n_neighbors, update_n_neighbors
knn_bp = Blueprint('knn', __name__)
training_progress = {'status': 'idle', 'percentage': 0}

def convert_to_url_path(path):
    # Normalisasi path
    normalized_path = os.path.normpath(path)
    # Ganti backslash dengan slash
    url_path = normalized_path.replace(os.sep, '/')
    return url_path

@knn_bp.route('/training-model', methods=['POST'])
def training_model():
    for category in ['formalin', 'non_formalin']:
        files = request.files.getlist(f'{category}_files')
        for file in files:
            if file and allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
                filename = secure_filename(file.filename)
                file_ext = filename.rsplit('.', 1)[1].lower()
                unique_filename = f"{uuid.uuid4().hex}.{file_ext}"
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], 'training', category, unique_filename))

    global training_progress
    training_progress = {'status': 'idle', 'percentage': 0}
    threading.Thread(target=train_model, args=(current_app._get_current_object(), training_progress)).start()
    return jsonify({'message': 'Training started', 'status': 'success'})

@knn_bp.route('/training-status', methods=['GET'])
def training_status():
    return jsonify(training_progress)

@knn_bp.route('/identifikasi', methods=['POST'])
def identifikasi():
    result = None
    if request.method == 'POST':
        file = request.files['test_file']
        if current_user.role == 'user':
            k_value = read_n_neighbors()
        else:
            k_value = int(request.form['k_value'])

        if file and allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
            filename = file.filename
            test_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'testing', filename)
            file.save(test_path)

            result = identify_image(test_path, k_value, 'data/training_data.csv')

    return jsonify({'result': result})

@knn_bp.route('/ekstraksi', methods=['POST'])
def ekstraksi():
    if request.method == 'POST':
        file = request.files['test_file']

        if file and allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
            filename = file.filename
            test_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'testing', filename)
            file.save(test_path)

            r, g, b = extract_rgb(test_path)
            h, s, v = rgb_to_hsv(r, g, b)
            image_path = process_image(test_path)

            hsv_values = [
                {'name': 'Hue', 'value': h},
                {'name': 'Saturation', 'value': s},
                {'name': 'Value', 'value': v},
            ]
            image_url = url_for('uploaded_file', filename=convert_to_url_path(image_path.replace('uploads/',
                                                                                                 '')))
            print(image_url)
            return jsonify({
                'features': hsv_values,
                'image_url': image_url
            })

    return jsonify({'error': 'Invalid request'}), 400

@knn_bp.route('/save-knn', methods=['POST'])
def save_knn():
    result = None
    if request.method == 'POST':
        data = request.get_json()  # Mengambil data JSON
        k_value = data.get('k_value')
        result = update_n_neighbors(k_value)
    return jsonify({'result' : result})
