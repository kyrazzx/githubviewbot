from concurrent.futures import ThreadPoolExecutor
import random
import time
import cloudscraper

banner = """
  ________.__  __     ___ ___      ___.     ____   ____.__              ___.           __   
 /  _____/|__|/  |_  /   |   \ __ _\_ |__   \   \ /   /|__| ______  _  _\_ |__   _____/  |_ 
/   \  ___|  \   __\/    ~    \  |  \ __ \   \   Y   / |  |/ __ \ \/ \/ /| __ \ /  _ \   __\
\    \_\  \  ||  |  \    Y    /  |  / \_\ \   \     /  |  \  ___/\     / | \_\ (  <_> )  |  
 \______  /__||__|   \___|_  /|____/|___  /    \___/   |__|\___  >\/\_/  |___  /\____/|__|  
        \/                 \/           \/                     \/            \/             
"""
print(banner)

url = input("Enter the URL to target > ")

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
]

use_proxies = input("Do you want to use proxies? (y/n) > ").lower() == 'y'

if use_proxies:
    try:
        with open("proxies.txt") as f:
            proxies_list = f.read().splitlines()
    except FileNotFoundError:
        print("[ERROR] proxies.txt not found. Please provide a valid proxy list.")
        exit()

    if not proxies_list:
        print("[ERROR] No proxies found in proxies.txt.")
        exit()
else:
    proxies_list = []

views = 0

def test():
    global views
    while True:
        proxy = random.choice(proxies_list) if use_proxies else None
        proxy_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else {}

        headers = {
            "User-Agent": random.choice(user_agents),
            "Referer": "https://github.com/",
        }

        try:
            scraper = cloudscraper.create_scraper(delay=10)
            response = scraper.get(url, headers=headers, proxies=proxy_dict)

            if response.status_code == 200:
                views += 1
                print(f"Total Views : {views}")
            else:
                print(f"[WARNING] Received status code {response.status_code}")

        except Exception as e:
            print(f"[ERROR] {e}")

        time.sleep(1)

with ThreadPoolExecutor(max_workers=100) as executor:
    for _ in range(100):
        executor.submit(test)
