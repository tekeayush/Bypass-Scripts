from time import sleep
from requests import Session as rsession
from bs4 import BeautifulSoup

url = input('URL: ')

def try2link(url):
    token = url.split('/')[-1]
    Domain = 'https://try2link.com/'
    client = rsession()
    resp = client.get(Domain+token, headers={"referer": 'https://trip.businessnews-nigeria.com/'})
    soup = BeautifulSoup(resp.content, "html.parser")
    inputs = soup.find(id="go-link").find_all(name="input")
    data = { input.get('name'): input.get('value') for input in inputs }
    h = { "x-requested-with": "XMLHttpRequest" }
    sleep(6)
    r = client.post(f"{Domain}links/go", data=data, headers=h)
    if r.json()['url']=='':
        return (r.json())
    else:
        return (r.json()['url'])

print(try2link(url))