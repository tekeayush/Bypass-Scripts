from time import sleep

import requests
from bs4 import BeautifulSoup

url='https://short-jambo.ink/ttlwT'

def shortjambo(url):    
    with requests.Session() as client:  
        ref = "https://forex0.aghtas.com/"   
        h = {"referer": ref}  
        resp = client.get(url,headers=h)   
        soup = BeautifulSoup(resp.content, "html.parser")    
        inputs = soup.find_all("input")   
        data = { input.get('name'): input.get('value') for input in inputs }
        h = { "x-requested-with": "XMLHttpRequest" }   
        sleep(10)
        r = client.post(f"https://short-jambo.ink/links/go", data=data, headers=h)
        return r.json()['url']

print(shortjambo(url))
