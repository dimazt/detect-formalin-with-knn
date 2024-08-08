import os
import cv2
import uuid
from werkzeug.utils import secure_filename

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def extract_rgb(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Gambar tidak ditemukan di path: {image_path}")
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height, width, _ = image_rgb.shape
    x, y = width // 2, height // 2
    r, g, b = image_rgb[y, x]
    return r, g, b

def extract_features(image_path):
    r, g, b = extract_rgb(image_path)
    h, s, v = rgb_to_hsv(r, g, b)
    return h, s, v

def convert_hsv_image(image_path):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_hsv = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2HSV)
    return image_hsv

def save_hsv_image(image_hsv, original_filename):
    filename = secure_filename(original_filename)
    file_ext = filename.rsplit('.', 1)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}.{file_ext}"
    hsv_path = os.path.join('uploads/hsv_image', unique_filename)
    cv2.imwrite(hsv_path, image_hsv)
    return hsv_path

def process_image(image_path):
    image_hsv = convert_hsv_image(image_path)
    hsv_image_path = save_hsv_image(image_hsv, os.path.basename(image_path))
    return hsv_image_path

def rgb_to_hsv(r, g, b):
    r_norm = r / 255.0
    g_norm = g / 255.0
    b_norm = b / 255.0
    c_max = max(r_norm, g_norm, b_norm)
    c_min = min(r_norm, g_norm, b_norm)
    delta = c_max - c_min

    if delta == 0:
        h = 0
    elif c_max == r_norm:
        h = 60 * (((g_norm - b_norm) / delta) % 6)
    elif c_max == g_norm:
        h = 60 * (((b_norm - r_norm) / delta) + 2)
    elif c_max == b_norm:
        h = 60 * (((r_norm - g_norm) / delta) + 4)
    if h < 0:
        h += 360

    s = (delta / c_max) if c_max != 0 else 0
    v = c_max
    return h, s, v
