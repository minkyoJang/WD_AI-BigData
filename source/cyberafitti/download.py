import requests
headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
          'Client-ID':'jzkbprff40iqj646a697cyrvl0zt2m6',
          "X-Device-Id": "4548433207d39f1d"}

def download(method, url, param=None, data=None):
    try:
        resp = requests.request(method, url,
                     params=param, data=data,
                     headers=headers)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e.response.status_code)
        print(e.response.reason)
    return resp