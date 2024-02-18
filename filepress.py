from urllib.parse import urlparse
import requests

url = input('url: ')

def filepress(url, api_url, api2_url):
    client = requests.session()
    try:
        res = client.get(url)
        res.raise_for_status()
        raw = urlparse(url)
        json_data = {
            'id': raw.path.split('/')[-1],
            'method': 'cloudR2Downlaod',
        }
        api = api_url
        api2 = api2_url

        res = client.post(api,
                          headers={
                              'Referer': f'{raw.scheme}://{raw.hostname}'
                          },
                          json=json_data)
        res.raise_for_status()  
    except requests.exceptions.RequestException as e:
        return f'ERROR: {e}'

    if 'data' not in res.json():
        return f'ERROR: {res.json()["statusText"]}'
    else:
        json_data = {
            'id': res.json()['data']['downloadId'],
            'method': 'cloudR2Downlaod',
        }
        res = client.post(api2,
                          headers={'Referer': f'{raw.scheme}://{raw.hostname}'},
                          json=json_data)
        res.raise_for_status()  
        if res.status_code == 200:
            return res.json()['data']
        else:
            return f'Failed At API2 With Status {res.json()["statusText"]}'


api_url = 'https://new9.filepress.store/api/file/downlaod/'
api2_url = 'https://new9.filepress.store/api/file/downlaod2/'

print(filepress(url, api_url, api2_url))


# alternate methods of downloads
#indexDownlaod
#cloudDownlaod
#cloudR2Downlaod (Best)
