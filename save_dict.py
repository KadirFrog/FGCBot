import json

def save_dict(d: dict):
    with open('dict.json', 'w') as f:
        json.dump(d, f)

def load_dict():
    with open('dict.json', 'r') as f:
        return json.load(f)
