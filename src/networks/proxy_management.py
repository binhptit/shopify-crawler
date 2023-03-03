import json
import queue
from typing import Dict

def load_json_file(file_path: str) -> Dict:
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

class ProxyPool:
    def __init__(self, proxies_data : str= './src/networks/assets/list_proxy.json', id_part : int = 0, num_of_part: int = 3) -> None:
        assert id_part < num_of_part, "id_part must be less than num_of_part"

        self.proxies = load_json_file(proxies_data)
        self.proxy_queue = queue.Queue()
        self.proxy_list = []
        for proxy in self.proxies:
            if "code" in self.proxies[proxy]:
                if self.proxies[proxy]["code"] not in ["HK", "CN", "TW"]:
                    self.proxy_list.append(proxy)
        
        self.proxy_list = self.split_list_into_multiple_parts(self.proxy_list, num_of_part)[id_part]

        for proxy in self.proxy_list:
            self.proxy_queue.put(proxy)

    def split_list_into_multiple_parts(self, list_data: list, num_of_part: int) -> list:
        return [list_data[i:i + len(list_data) // num_of_part] for i in range(0, len(list_data), len(list_data) // num_of_part)]

    def get_size_queue(self):
        return self.proxy_queue.qsize()

    def get_proxy(self) -> str:
        proxy = None

        while not self.proxy_queue.empty():
            proxy = self.proxy_queue.get()
            break
        
        return proxy

    def put_proxy(self, proxy: str) -> None:
        self.proxy_queue.put(proxy)