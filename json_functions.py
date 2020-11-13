import json
import os


USER_DATA_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'user_data.json'
)


def load_data(user_data):
    with open(USER_DATA_PATH, 'w') as f:
        json.dump(user_data, f)


def download_data():
    with open(USER_DATA_PATH) as f:
        return json.load(f)
