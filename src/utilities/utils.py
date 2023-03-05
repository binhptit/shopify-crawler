import json
import jsondiff
import unicodedata
from typing import Dict, List, Any
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
    
def read_json(filename: str) -> Dict:
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def compare_json(json_data_1 , json_data_2):
    if isinstance(json_data_1, str):
        json_data_1 = read_json(json_data_1)

    if isinstance(json_data_2, str):
        json_data_2 = read_json(json_data_2)

    diff = jsondiff.diff(json_data_1, json_data_2, syntax='explicit')
    return diff

def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=4)

def get_leaf_nodes(json_tree):
    if isinstance(json_tree, dict):
        return [leaf for node in json_tree.values() for leaf in get_leaf_nodes(node)]
    elif isinstance(json_tree, list):
        return [leaf for node in json_tree for leaf in get_leaf_nodes(node)]
    else:
        return [json_tree]

def check_containing_cjk_character(text):
    for character in text:
        name = unicodedata.name(character)
        if "CJK UNIFIED" in name \
            or "HIRAGANA" in name \
            or "KATAKANA" in name:
            return True
    return False

def filter_string_uppercase_or_space(text):
    return ''.join([c for c in text if c.isupper() or c == ' ' or check_containing_cjk_character(c)])

def keep_number(string):
    return ''.join(filter(str.isdigit, string))

def save_string_json(filename, data):
    json_string = json.dumps(data, cls=JSONEncoder, indent=4, ensure_ascii=False)

    with open(filename, "w", encoding='utf-8') as f:
        f.write(json_string)

def extract_key_values(tree, key):
    if isinstance(tree, dict):
        for k, v in tree.items():
            if k == key:
                yield v
            else:
                yield from extract_key_values(v, key)
    elif isinstance(tree, list):
        for item in tree:
            yield from extract_key_values(item, key)

def check_containing_cjk_character(text):
    for character in text:
        name = unicodedata.name(character)
        if "CJK UNIFIED" in name \
            or "HIRAGANA" in name \
            or "KATAKANA" in name:
            return True
    return False

def filter_uncasual_slug(text):
    return ''.join([c for c in text if c.isupper() or c == ' ' or check_containing_cjk_character(c)])

