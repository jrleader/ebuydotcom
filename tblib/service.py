# service.py

# Provide Serialization of request params,
# Deserialization of responses,
# Response code checking

import requests

class ServiceResponseNotOk(Exception):
    pass

class Service(requests.Session):
    def __init__(self,app,timeout=5):
        super().__init__()

        self.app = app
        self.timeout = timeout

    @property
    def base_url(self):
        '''
        To be overriden by subclasses, so custom base urls can be constructed
        '''

        return ''

    def check_code(self,json):
        '''
        Check the response code in the json, raise exceptions if needed
        '''

        if json['code'] != 0:
            raise ServiceResponseNotOk('Abnormal service response! Code: {}, Message: {}'.format(json['code'],json['message']))

    def get(self, path, **kwargs):

        '''
        Make requests with completed URLs
        '''
        url = self.base_url + path
        kwargs.setdefault('timeout', self.timeout)
        return super().get(url, **kwargs) # GET request

    def get_json(self, path, check_code=True, **kwargs):
        '''
        Get json responses
        '''
        resp = self.get(path, **kwargs)

        json = resp.json()

        if check_code:
            self.check_code(json)

        return json
    
    def post(self, path, data=None, json=None, **kwargs):
        '''
        Make POST requests
        '''
        url = self.base_url + path
        kwargs.setdefault('timeout', self.timeout)
        return super().post(url,data,json,**kwargs)

    def post_json(self,path,data=None,json=None,check_code=True,filter_none_field=True,**kwargs):

        # Prepare request params
        if isinstance(data,dict) and filter_none_field:
            data = {k:v for k,v in data.items() if v is not None}
        if isinstance(json, dict) and filter_none_field:
            json = {k:v for k,v in json.items() if v is not None}
        
        resp = self.post(path, data, json, **kwargs) 

        json = resp.json()

        if check_code:
            self.check_code(json)

        return json

    def delete(self, path, **kwargs):
        '''
        Make DELETE requests
        '''
        url = self.base_url + path
        kwargs.setdefault('timeout', self.timeout)
        return super().delete(url, **kwargs)


    def delete_json(self, path, check_code=True, **kwargs):
        resp = self.delete(path, **kwargs)
        json = resp.json()

        if check_code:
            self.check_code(json)
        
        return json