# proxy_free_collector.py
import requests
import threading
import queue
import random
from concurrent.futures import ThreadPoolExecutor
import re

class FreeProxyCollector:
    def __init__(self):
        self.proxies = []
        self.working_proxies = []
        self.proxy_queue = queue.Queue()
        
        self.proxy_sources = [
            "https://api.proxyscrape.com/v4/free-proxy-list/get?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
            "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
            "https://www.proxy-list.download/api/v1/get?type=http",
            "https://www.sslproxies.org/",
            "https://free-proxy-list.net/",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
        ]
        
        self.test_sites = [
            "http://httpbin.org/ip",
            "https://api.ipify.org",
        ]
        
    def collect_all_proxies(self):
        print("[*] Colleziono proxy...")
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(self.fetch_source, self.proxy_sources)
        for proxy_list in results:
            if proxy_list:
                self.proxies.extend(proxy_list)
        self.proxies = list(set(self.proxies))
        print(f"[+] Proxy collezionati: {len(self.proxies)}")
        return self.proxies
    
    def fetch_source(self, url):
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 200:
                return self.parse_proxies(r.text)
        except:
            pass
        return []
    
    def parse_proxies(self, text):
        proxies = []
        pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}:\d{2,5}\b'
        matches = re.findall(pattern, text)
        for match in matches:
            if self.validate_proxy(match):
                proxies.append(match)
        return proxies
    
    def validate_proxy(self, proxy):
        try:
            ip, port = proxy.split(':')
            parts = ip.split('.')
            if len(parts) != 4:
                return False
            for p in parts:
                if not p.isdigit() or int(p) > 255:
                    return False
            if not port.isdigit() or int(port) < 1 or int(port) > 65535:
                return False
            return True
        except:
            return False
    
    def test_proxy(self, proxy):
        try:
            proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
            r = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=5)
            return r.status_code == 200
        except:
            return False
    
    def test_proxies_parallel(self, max_workers=30):
        print(f"[*] Testo {len(self.proxies)} proxy...")
        self.working_proxies = []
        lock = threading.Lock()
        
        def test_one(p):
            if self.test_proxy(p):
                with lock:
                    self.working_proxies.append(p)
                    print(f"[+] Proxy OK: {p}")
        
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            ex.map(test_one, self.proxies[:200])
        
        print(f"[+] Proxy funzionanti: {len(self.working_proxies)}")
        return self.working_proxies
    
    def get_random_proxy(self):
        if not self.working_proxies:
            self.collect_all_proxies()
            self.test_proxies_parallel()
        return random.choice(self.working_proxies) if self.working_proxies else None
