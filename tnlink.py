from time import sleep
import requests
from bs4 import BeautifulSoup


def tnlink(url:str):
    url = url[:-1] if url[-1] == '/' else url
    token = url.split("/")[-1]
    client = requests.Session()
    ref = "https://jrlinks.in/"   
    domain = "https://go.tnshort.net/"
    h = {"referer": ref} 
    response = client.get(domain+token, headers=h)
    soup = BeautifulSoup(response.content, "html.parser")
    inputs = soup.find(id="go-link").find_all(name="input")
    data = { input.get('name'): input.get('value') for input in inputs }
    sleep(8)
    headers={"x-requested-with": "XMLHttpRequest"}
    return client.post(domain+"links/go", data=data, headers=headers).json()["url"] 
