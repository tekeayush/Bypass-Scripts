from cfscrape import create_scraper
from urllib.parse import urlparse

url = input('url: ')

def filepress(url):
    cget = create_scraper().request
    try:
        url = cget('GET', url).url
        raw = urlparse(url)
        json_data = {
            'id': raw.path.split('/')[-1],
            'method': 'cloudR2Downlaod',
            }
        api = f'{raw.scheme}://{raw.hostname}/api/file/downlaod/'
        api2 = f'https://new8.filepress.store/api/file/downlaod2/'
        res = cget('POST', api, headers={'Referer': f'{raw.scheme}://{raw.hostname}'}, json=json_data).json()
    except Exception as e:
        return(f'ERROR: {e.__class__.__name__}')
    if 'data' not in res:
        return(f'ERROR: {res["statusText"]}')
    else:
        json_data = {
            'id': res['data']['downloadId'],
            'method': 'cloudR2Downlaod',
            }
        res = cget('POST', api2, headers={'Referer': f'{raw.scheme}://{raw.hostname}'}, json=json_data)
        if res.status_code == 200:
            return res.json()['data']
        else:
            return f'Failed At API2 With Status {res.json()["statusText"]}'
print(filepress(url))
