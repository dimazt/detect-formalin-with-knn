import os
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score
from utils.image_processing import allowed_file, extract_features, extract_rgb, rgb_to_hsv

def train_model(app, training_progress):
    training_progress['status'] = 'running'
    training_progress['percentage'] = 0
    training_data = []
    labels = []

    for category in ['formalin', 'non_formalin']:
        label = 1 if category == 'formalin' else 0
        category_path = os.path.join(app.config['UPLOAD_FOLDER'], 'training', category)
        files = [f for f in os.listdir(category_path) if allowed_file(f, app.config['ALLOWED_EXTENSIONS'])]

        for idx, filename in enumerate(files):
            image_path = os.path.join(category_path, filename)
            try:
                h, s, v = extract_features(image_path)
                training_data.append([h, s, v])
                labels.append(label)
                progress = int((idx + 1) / len(files) * 100)
                training_progress['percentage'] = progress
            except Exception as e:
                print(f"Error processing {image_path}: {e}")

    df = pd.DataFrame(training_data, columns=['H', 'S', 'V'])
    df['label'] = labels
    df.to_csv('models/training_data.csv', index=False)

    X = df[['H', 'S', 'V']].values
    y = df['label'].values
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    knn = KNeighborsClassifier(n_neighbors=1)
    knn.fit(x_train, y_train)

    y_pred = knn.predict(x_test)
    cm = confusion_matrix(y_test, y_pred)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"Confusion Matrix:\n{cm}")
    print(f"Accuracy: {accuracy:.2f}")

    training_progress['status'] = 'completed'
    training_progress['percentage'] = 100

def identify_image(image_path, k_value, training_data_path):
    r, g, b = extract_rgb(image_path)
    h, s, v = rgb_to_hsv(r, g, b)

    train_data = pd.read_csv(training_data_path)
    x_train = train_data[['H', 'S', 'V']].values
    y_train = train_data['label'].values

    knn = KNeighborsClassifier(n_neighbors=k_value)
    knn.fit(x_train, y_train)

    prediction = knn.predict([[h, s, v]])
    return "Berformalin" if prediction[0] == 1 else "Tidak Berformalin"
