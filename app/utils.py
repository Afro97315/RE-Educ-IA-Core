# app/utils.py
import os
import json

def load_json_data(filename):
    base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', filename)
    with open(base_path, 'r', encoding='utf-8') as f:
        return json.load(f)
