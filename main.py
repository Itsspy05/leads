import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time
import threading
import json
import logging

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# User-Agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (Linux; Android 11)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
    "Mozilla/5.0 (X11; Linux x86_64)"
]

# Authenticated proxies (IP:PORT:USER:PASS)
def get_authenticated_proxy():
    raw_proxies = [
        "38.153.152.244:9594:jchiqzjh:4ps7yatleu4t",
        "86.38.234.176:6630:jchiqzjh:4ps7yatleu4t",
        "173.211.0.148:6641:jchiqzjh:4ps7yatleu4t",
        "216.10.27.159:6837:jchiqzjh:4ps7yatleu4t",
        "154.36.110.199:6853:jchiqzjh:4ps7yatleu4t",
        "45.151.162.198:6600:jchiqzjh:4ps7yatleu4t",
        "188.74.210.3:6082:jchiqzjh:4ps7yatleu4t",
        "188.74.210.207:6286:jchiqzjh:4ps7yatleu4t",
        "188.74.210.21:6100:jchiqzjh:4ps7yatleu4t",
        "91.246.195.196:6965:jchiqzjh:4ps7yatleu4t"
    ]
    proxy = random.choice(raw_proxies).strip()
    ip, port, user, pwd = proxy.split(":")
    proxy_formatted = f"http://{user}:{pwd}@{ip}:{port}"
    return {
        "http": proxy_formatted,
        "https": proxy_formatted
    }

# Lead storage
leads = []

# Scrape logic
def scrape_data(url, keywords, location):
    headers = {"User-Agent": random.choice(user_agents)}
    proxies = get_authenticated_proxy()
    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for i in range(random.randint(3, 5)):
                lead = {
                    'Name': f'User_{random.randint(1000, 9999)}',
                    'Bio': 'Interested in ' + random.choice(keywords),
                    'Location': location
                }
                leads.append(lead)
        else:
            logging.warning(f"Failed to fetch {url}: {response.status_code}")
    except Exception as e:
        logging.error(f"Error scraping {url}: {e}")

# Filter logic
def filter_leads(leads, criteria):
    filtered = []
    seen = set()
    for lead in leads:
        key = (lead['Name'], lead['Location'])
        if key in seen:
            continue
        seen.add(key)
        if any(k.lower() in lead['Bio'].lower() for k in criteria['keywords']):
            filtered.append(lead)
    return filtered

# Export CSV + JSON
def export_leads(leads, prefix="filtered_leads"):
    df = pd.DataFrame(leads)
    df.to_csv(f"{prefix}.csv", index=False)
    with open(f"{prefix}.json", 'w') as f:
        json.dump(leads, f, indent=4)
    logging.info(f"Exported {len(leads)} leads to {prefix}.csv and .json")

# Main function
def run_scraper():
    urls = [
        "https://www.reddit.com/r/WorkOnline/",
        "https://www.reddit.com/r/EntrepreneurRideAlong/",
        "https://www.reddit.com/r/digital_marketing/",
        "https://www.reddit.com/r/SideHustle/",
        "https://www.quora.com/topic/Online-Earning",
        "https://www.facebook.com/groups/digitalearninggroup/",
        "https://www.facebook.com/groups/affiliateearning/",
        "https://twitter.com/search?q=earn%20money%20online&src=typed_query",
        "https://www.pinterest.com/search/pins/?q=make%20money%20online",
        "https://medium.com/tag/make-money-online"
    ]
    keywords = ['earn', 'income', 'freelance', 'work from home', 'affiliate', 'crypto']
    location = 'India'

    threads = []
    for url in urls:
        t = threading.Thread(target=scrape_data, args=(url, keywords, location))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    criteria = {"keywords": keywords}
    filtered = filter_leads(leads, criteria)
    export_leads(filtered)

run_scraper()
