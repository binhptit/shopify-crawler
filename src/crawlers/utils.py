import json
import bs4

def filter_string(string: str, characters: str) -> str:
    return ''.join([c for c in string if c in characters])

def read_json(filename):
    with open(filename, 'r', encoding='utf-8') as infile:
        return json.load(infile)

def get_data_from_soup(web_data):
    text_results = []
    if isinstance(web_data, bs4.element.ResultSet):
        for result_set_data in web_data:
            if result_set_data.text.strip():
                text_results.append(result_set_data.text.strip())
    else:
        text_results.append(web_data.text.strip())
    
    return text_results

def palindrom_number(number):
    return str(number) == str(number)[::-1]
