import json
def filter_string(string: str, characters: str) -> str:
    return ''.join([c for c in string if c in characters])

def read_json(filename):
    with open(filename, 'r', encoding='utf-8') as infile:
        return json.load(infile)