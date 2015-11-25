__author__ = 'techbk'
# class gui file pcap

#from old__htmlclient import My_HttpClient

import requests
from . import config
#import json



class HTTPClient(object):
    def __init__(self, base_url):
        self.base_url = base_url


    def _update_headers(self, headers):
        if not headers:
            headers = {}
        content_type = headers.get('content-type', 'application/json; charset=utf-8')
        headers['content-type'] = content_type

        return headers


    def get(self, url, data=None, headers = None, json = None):
        headers = self._update_headers(headers)

        return requests.get(self.base_url + url,data=data, headers=headers ,json=json)



class Client(object):
    def __init__(self,q , base_url=None):
        #self._queue = q
        if not base_url:
            base_url = config.SERVICE_URL
        self.http_client = HTTPClient(base_url)


    def get_project_log(self, data):

        self.http_client.get(url='/projectlog', data=data)



if __name__ == "__main__":
    client = Client()
    r = client.get_project_log()
    print("################")
    print(r.text)
    print(r.headers)
    print(r.url)
    print(r.status_code)