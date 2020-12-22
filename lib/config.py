import json

def Config():
    config = json.load(open('config.json', 'r'))
    return config
