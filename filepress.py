import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re

def extract_file_id(url):
    raw = urlparse(url)
    return raw.path.strip('/').split('/')[-1], f"{raw.scheme}://{raw.hostname}"

def telegram_download(file_id, referer, api_url, tele_api_base, client):
    try:
        res = client.post(api_url,
                          headers={'Referer': referer},
                          json={'id': file_id, 'method': 'telegramDownload'})
        res.raise_for_status()
        data = res.json()
        if 'data' not in data:
            return f"Telegram API error: {data.get('statusText', 'Unknown error')}"

        start_param = data['data']
        tele_page_url = f"{tele_api_base}{start_param}"

        page = client.get(tele_page_url)
        page.raise_for_status()
        soup = BeautifulSoup(page.text, "html.parser")
        scripts = soup.find_all("script")

        for script in scripts:
            match = re.search(r"const\s+botName\s*=\s*['\"]([^'\"]+)['\"]", script.text)
            if match:
                bot_name = match.group(1)
                return f"https://telegram.me/{bot_name}?start={start_param}"

        return "Telegram bot name not found in page."
    except requests.exceptions.RequestException as e:
        return f"Telegram request error: {e}"
    except Exception as e:
        return f"Telegram unexpected error: {e}"

def cloud_download(file_id, referer, api_url_1, api_url_2, client):
    try:
        res1 = client.post(api_url_1,
                           headers={'Referer': referer},
                           json={'id': file_id, 'method': 'cloudR2Downlaod'})
        res1.raise_for_status()
        data1 = res1.json()
        if 'data' not in data1:
            return f"Cloud API1 error: {data1.get('statusText', 'Unknown error')}"

        download_id = data1['data'].get('downloadId')
        if not download_id:
            return "Cloud API1: downloadId missing."

        res2 = client.post(api_url_2,
                           headers={'Referer': referer},
                           json={'id': download_id, 'method': 'cloudR2Downlaod'})
        res2.raise_for_status()
        data2 = res2.json()
        if 'data' in data2:
            return data2['data']
        else:
            return f"Cloud API2 error: {data2.get('statusText', 'Unknown error')}"
    except requests.exceptions.RequestException as e:
        return f"Cloud request error: {e}"
    except Exception as e:
        return f"Cloud unexpected error: {e}"

def main():
    url = input("Enter Filepress URL: ").strip()
    print("\nSelect download method:")
    print("1. Cloud")
    print("2. Telegram")
    print("3. Both")
    option = input("Enter choice (1/2/3): ").strip()
    file_id, referer = extract_file_id(url)
    client = requests.Session()
    tele_api_base = 'https://tgfiles.shop/?start='
    cloud_api_url_1 = 'https://new3.filepress.live/api/file/downlaod/'
    cloud_api_url_2 = 'https://new3.filepress.live/api/file/downlaod2/'
    if option == '1':
        result = cloud_download(file_id, referer, cloud_api_url_1, cloud_api_url_2, client)
        print("\nCloud Download Link:\n", result)

    elif option == '2':
        result = telegram_download(file_id, referer, cloud_api_url_1, tele_api_base, client)
        print("\nTelegram Download Link:\n", result)

    elif option == '3':
        tele_result = telegram_download(file_id, referer, cloud_api_url_1, tele_api_base, client)
        cloud_result = cloud_download(file_id, referer, cloud_api_url_1, cloud_api_url_2, client)
        print("\nTelegram Download Link:\n", tele_result)
        print("\nCloud Download Link:\n", cloud_result)

    else:
        print("\nInvalid option. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
