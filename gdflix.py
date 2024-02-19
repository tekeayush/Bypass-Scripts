from urllib.parse import urlparse
import requests as rq
from lxml import etree
from bs4 import BeautifulSoup
import re

url = 'https://new.gdflix.ink/file/gZ4ppTXioz'


def gdflix_bypass(url: str):
  try:
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    client = rq.session()
    url = client.get(url, headers=headers).url
    raw = urlparse(url)
    res = client.get(url, headers=headers)
  except Exception as e:
    return (f'ERROR: {e.__class__.__name__}')
  try:
    soup = BeautifulSoup(res.text, 'html.parser')
    llist = soup.find_all('a')
    list = []
    for link in llist:
      href_attribute = link.get('href')
      if 'instant' in href_attribute:
        list.append(href_attribute)
    raw = urlparse(list[0])
    api = 'https://xtrocdn.zencloud.lol/api'
    resp = client.post(api, data={'keys': raw.query.split('=')[1]}).json()['url']
    return resp
  except Exception:
    key = re.findall('"key",\s+"(.*?)"', res.text)
    if not key:
      return ("ERROR: Key not found!")
    key = key[0]
    if not etree.HTML(res.content).xpath("//button[@id='drc']"):
      return ("This link don't have direct download button")
  headers = {
      'Content-Type':
      'multipart/form-data; boundary=----WebKitFormBoundaryi3pOrWU7hGYfwwL4',
      'User-Agent':
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
      'x-token': raw.hostname,
  }
  data = '------WebKitFormBoundaryi3pOrWU7hGYfwwL4\r\nContent-Disposition: form-data; name="action"\r\n\r\ndirect\r\n' \
      f'------WebKitFormBoundaryi3pOrWU7hGYfwwL4\r\nContent-Disposition: form-data; name="key"\r\n\r\n{key}\r\n' \
      '------WebKitFormBoundaryi3pOrWU7hGYfwwL4\r\nContent-Disposition: form-data; name="action_token"\r\n\r\n\r\n' \
      '------WebKitFormBoundaryi3pOrWU7hGYfwwL4--\r\n'
  try:
    res = client.post(url, cookies=res.cookies, headers=headers, data=data).json()['url']
    if res:
      resp = client.get(res, headers=headers)
      soup = BeautifulSoup(resp.content, 'html.parser')
      pattern = re.compile(r"let worker_url = '(.*?)';")
      match = pattern.search(resp.text)
      if match:
        worker_link = match.group(1)
        return worker_link
  except Exception as e:
    return e


print(gdflix_bypass(url))
