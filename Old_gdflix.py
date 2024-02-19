import requests as rq
from urllib.parse import urlparse
from lxml import etree
import re
from bs4 import BeautifulSoup

def gdflix_bypass(url:str):
    try:
        headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        client = rq.session()
        url = client.get(url, headers=headers).url
        raw = urlparse(url)
        res = client.get(url, headers=headers)
    except Exception as e:
        return(f'ERROR: {e.__class__.__name__}')
    key = re.findall('"key",\s+"(.*?)"', res.text)
    if not key:
        return("ERROR: Key not found!")
    key = key[0]
    if not etree.HTML(res.content).xpath("//button[@id='drc']"):
        return("This link don't have direct download button")
    headers = {
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryi3pOrWU7hGYfwwL4',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'x-token': raw.hostname,
    }
    data = '------WebKitFormBoundaryi3pOrWU7hGYfwwL4\r\nContent-Disposition: form-data; name="action"\r\n\r\ndirect\r\n' \
        f'------WebKitFormBoundaryi3pOrWU7hGYfwwL4\r\nContent-Disposition: form-data; name="key"\r\n\r\n{key}\r\n' \
        '------WebKitFormBoundaryi3pOrWU7hGYfwwL4\r\nContent-Disposition: form-data; name="action_token"\r\n\r\n\r\n' \
        '------WebKitFormBoundaryi3pOrWU7hGYfwwL4--\r\n'
    try:
        res = client.post(url, cookies=res.cookies, headers=headers, data=data).json()['url']
        resp = client.get(res).text
        soup = BeautifulSoup(resp, 'html.parser')
        drive = soup.find('form')
        return drive.get('action')
    except Exception as e:
        if res.status_code == 200:
            return drive
        elif e.__class__.__name__ == 'KeyError':
            return 'File Not Found'
        else:
            return res
