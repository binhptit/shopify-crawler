from typing import Dict
from bs4 import BeautifulSoup
import numpy as np
from urllib.request import Request, urlopen
import bs4
import json
import requests

def save_json_file(file_name: str, data: Dict):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)

def is_alive_proxy(proxy_ip: str):
    try:
        response = requests.get("https://www.google.com/", proxies={"http": f"http://{proxy_ip}"})
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as error:
        return False

def crawl_proxies_1(retries = 3):
    while retries:
        try:
            req = Request(url='https://free-proxy-list.net/', 
            headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            break
        except Exception as e:
            retries -= 1
            print(f"Retrying {retries} times!")

    if not retries:
        return {}
    
    soup = BeautifulSoup(webpage, 'html.parser')
    web_data = soup.find('table', class_='table table-striped table-bordered').find_all('tr')

    proxy_dict = {}
    for tr_data in web_data:
        td_data = tr_data.find_all('td')
    
        proxy_infos = []
        if isinstance(td_data, bs4.element.ResultSet):
            for result_set_data in td_data:
                if result_set_data.text.strip():
                    proxy_infos.append(result_set_data.text.strip())
        
        if len(proxy_infos):
            try: 
                proxy_dict[f"{proxy_infos[0]}:{proxy_infos[1]}"] = {
                    "code": proxy_infos[2],
                    "country": proxy_infos[3],
                    "anonymity": proxy_infos[4],
                    "google": proxy_infos[5],
                    "https": proxy_infos[6],
                    "last_checked": proxy_infos[7]
                    }

            except IndexError:
                continue

    return proxy_dict      
                
def crawl_proxies_2(retries = 3):
    proxy_dict = {}

    while retries:
        try:
            req = Request(url='https://hidemy.name/en/proxy-list/', 
            headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            break
        except Exception as e:
            retries -= 1
            print(f"Retrying {retries} times!")
    
    if not retries:
        return {}
    
    soup = BeautifulSoup(webpage, 'html.parser')
    web_data = soup.find('div', class_='table_block').find_all('tr')

    for tr_data in web_data:
        td_data = tr_data.find_all('td')
    
        proxy_infos = []
        if isinstance(td_data, bs4.element.ResultSet):
            for result_set_data in td_data:
                if result_set_data.text.strip():
                    proxy_infos.append(result_set_data.text.strip())
        
        if len(proxy_infos) > 6:
            proxy_dict[f"{proxy_infos[0]}:{proxy_infos[1]}"] = {
                "country": proxy_infos[2],
                "speed": proxy_infos[3],
                "typle": proxy_infos[4],
                "anonymity": proxy_infos[5],
                "last_checked": proxy_infos[6]
                }
            
    return proxy_dict

def crawl_proxies_3(get_max = 500, retry = 3):
    def is_ip(ip):
        try:
            return str(int(ip.split('.')[0])) == ip.split('.')[0] and 0 <= int(ip.split('.')[0]) <= 255 and \
                    str(int(ip.split('.')[1])) == ip.split('.')[1] and 0 <= int(ip.split('.')[1]) <= 255 and \
                    str(int(ip.split('.')[2])) == ip.split('.')[2] and 0 <= int(ip.split('.')[2]) <= 255 
        except:
            return False
 
    while retry:
        try:
            req = Request(url='https://github.com/TheSpeedX/PROXY-List/blob/master/http.txt', 
            headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            break
        except Exception as e:
            print(e)
            retry -= 1
    
    if not retry:
        return {}

    soup = BeautifulSoup(webpage, 'html.parser')
    web_data = soup.find_all('td', class_='blob-code blob-code-inner js-file-line')

    proxy_dict = {}
    for tr_data in web_data:
        if is_ip(tr_data.text.strip()) and is_alive_proxy(tr_data.text.strip()):        
            proxy_dict[f"{tr_data.text.strip()}"] = {
                "country": "N/A",
                "speed": "N/A",
                "uptime": "N/A",
                "anonymity": "N/A",
                "last_checked": "N/A"
                }
            
            get_max -= 1
            if not get_max:
                break

        else:
            print("FAILED")

    return proxy_dict

if __name__ == "__main__":
    merged_dict = crawl_proxies_1()
    merged_dict.update(crawl_proxies_2())
    merged_dict.update(crawl_proxies_3())

    save_json_file("src/networks/assets/list_proxy.json", merged_dict)

