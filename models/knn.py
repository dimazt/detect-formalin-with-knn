import json

json_path = 'data/knn.json'

def create_n_neighbors(n_neighbors):
    """Create or update the n_neighbors value in the JSON file."""
    with open(json_path, 'w') as json_file:
        json.dump({"n_neighbors": n_neighbors}, json_file)

def read_n_neighbors():
    """Read the n_neighbors value from the JSON file."""
    try:
        with open(json_path, 'r') as json_file:
            data = json.load(json_file)
            return data.get("n_neighbors")
    except FileNotFoundError:
        return None

def update_n_neighbors(k_value):
    try:
        k_value = int(k_value)
        create_n_neighbors(k_value)
        return {'status': 'success', 'k_value': k_value}
    except ValueError:
        return {'status': 'error', 'message': 'Invalid k_value'}