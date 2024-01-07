from time import sleep

import requests
from bs4 import BeautifulSoup


def ez4short_bypass(url):    
    with requests.Session() as client:
        DOMAIN = "https://ez4short.com"     
        ref = "https://ez4mods.com/"   
        h = {"referer": ref}  
        resp = client.get(url,headers=h)   
        soup = BeautifulSoup(resp.content, "html.parser")    
        inputs = soup.find_all("input")   
        data = { input.get('name'): input.get('value') for input in inputs }
        h = { "x-requested-with": "XMLHttpRequest" }   
        sleep(8)
        r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
        return r.json()['url']
