import os
import threading
from flask import Blueprint, request, jsonify, url_for, current_app
from utils.image_processing import allowed_file, process_image, extract_rgb, rgb_to_hsv
from utils.knn_model import train_model, identify_image
from werkzeug.utils import secure_filename
import uuid
knn_bp = Blueprint('knn', __name__)
training_progress = {'status': 'idle', 'percentage': 0}

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
        k_value = int(request.form['k_value'])

        if file and allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
            filename = file.filename
            test_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'testing', filename)
            file.save(test_path)

            result = identify_image(test_path, k_value, 'models/training_data.csv')

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
            image_url = url_for('uploaded_file', filename=image_path.replace('uploads/', ''))
            return jsonify({
                'features': hsv_values,
                'image_url': image_url
            })

    return jsonify({'error': 'Invalid request'}), 400
