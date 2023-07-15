import json


def read_json_file(file_path, encoding='utf-8'):
    with open(file_path, 'r', encoding=encoding) as file:
        data = json.load(file)
        json_string = json.dumps(data)
    return json_string
