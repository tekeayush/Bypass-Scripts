from requests import Session as rsession
from bs4 import BeautifulSoup as bs4
from gdflix import gdflix_bypass


def appdrive(url):
    if 'file' in url:
        return(gdflix_bypass(url))
    else:
        client = rsession()
        resp = client.get(url, verify=False)
        soup = bs4(resp.content, 'html.parser')
        content = soup.find_all('a', target='_blank')
        link = 'https://appdrive.lol'
        listt=[]
        for i in content:
            f=i.get('href')
            if 'file' in f:
                listt.append(link+f)
        for link in listt:
            return link
