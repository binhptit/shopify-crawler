import requests
import urllib
from proxy_management import ProxyPool

class RequestRouter:
    def __init__(self) -> None:
        self.proxy_pool = ProxyPool()

    def get_request(self, url):
        try:
            proxy = self.proxy_pool.get_proxy()
            with requests.Session() as session:
                response = session.get(url, proxies={'http': f"http://{proxy}"})
        except Exception as e:
            response = urllib.request.urlopen(url)
            proxy = None
            print("Exception:", e)

        if proxy:
            self.proxy_pool.put_proxy(proxy)
            
        return response
    

