
from abc import abstractclassmethod
from .errors import ApiErrorException
from .endpoint import ProvincesEndpoint, CitiesEndpoint, CostEndpoint
import requests
import json
from json.encoder import JSONEncoder

"""_summary_

Base class for API client.



Raises:
    ApiErrorException: If the API returns an error.

Returns:
    _type_: object - The return type of the function.
"""


class ClientOptions:
    """_summary_
    Options to configure the client.
    
    Attributes:
    auth: Bearer token for authentication. If left undefined, the `auth` parameter should be set on each request.
    accout_type: Account type to use.
    base_url: The root URL for sending API requests. This can be changed to test with a mock server.
    """
    
    auth = None
    account_type = ["starter", "basic", "pro"]
    base_url = {
        "starter": "http://api.rajaongkir.com/starter/",
        "basic": "http://api.rajaongkir.com/basic/",
        "pro": "http://pro.rajaongkir.com/api/",
    }
    courier = {
        "JNE": "jne",
        "POS": "pos",
        "TIKI": "tiki",
        "ALL_COURIER": "all",
    }


class BaseClient:
    key_list = "rajaongkir"
    
    def __init__(self, auth=None, account_type="starter"):
        
        self.provinces = ProvincesEndpoint(self)
        self.cities = CitiesEndpoint(self)
        self.cost = CostEndpoint(self)
    
    def _grab(cls, json_results):
        return json_results.get(cls.key_list)
    
    
    def _status(self, response_json):
        if not response_json:
            raise ApiErrorException("Response Api is None, cannot fetch the status of api")
        
        status = response_json.get("status")
        
        assert status is not None, 'Response Status is not Available'
        
        assert status.get("code") == requests.codes.ok, 'Response status not clear, should be any error occurred: {}'.format(status.get('description'))
        
    def _parse_response(self, response_json):
        return response_json.get('results') if response_json is not None else None
        
    @abstractclassmethod
    def request(self, params=None):
        pass


class Client(BaseClient):
    """Syncronous request to the API.

    Args:
        BaseClient (_type_): _description_
    
    Methods:
        get: get request to the API.
        post: post request to the API.
        put: put request to the API.
        delete: delete request to the API.
        options: options request to the API.
        
        requests: requests to the API.

    Raises:
        ApiErrorException: If the API returns an error.

    Returns:
        _type_: _description_
    """
    json_encoder = JSONEncoder
    
    def __init__(self, auth = ClientOptions.auth, account_type = ClientOptions.account_type[0]) -> None:
        if account_type not in ClientOptions.account_type:
            raise ValueError(
                f"Account type must be one of {ClientOptions.account_type}"
            )
        self.account_type = account_type
        
        if auth is None:
            auth = ClientOptions.auth
        
        self.auth = auth
        self.base_url = ClientOptions.base_url[account_type]
        
        
        super().__init__(self.auth, self.account_type)
    
    def get(self, headers=None, url_parameters={}):
        return requests.get(
            self.base_url,
            params=url_parameters,
            headers=headers
        )

    def post(self, headers=None, params={}, payload={}):
        return requests.post(
            self.base_url, 
            headers=headers, 
            params=params, 
            data=json.dumps(payload, cls=self.json_encoder)
        )
    
    def put(self, headers=None, params={}, payload={}):
        return requests.put(self.base_url, headers=headers, params=params, data=json.dumps(payload, cls=self.json_encoder))
    
    def delete(self, headers=None, params={}):
        return requests.delete(self.base_url, headers=headers, params=params)
    
    def options(self, headers=None, params={}):
        return requests.options(self.base_url, headers=headers, params=params)
    
    def request(self, **kwargs):
        req_params = {
            'headers': {
                'Accept': 'application/json',
                'key': self.auth
            }
        }
        
        if kwargs.get('params') is not None:
            req_params['url_parameters'] = kwargs.get('params')
            
        self.base_url = ClientOptions.base_url[self.account_type]
        self.base_url = self.base_url + kwargs.get('endpoint')
        
        if kwargs.get('pyload') is not None:
            response = self.post(kwargs.get('headers'), kwargs.get('params'), kwargs.get('pyload'))
        else:
            response = self.get(**req_params)

        return self._grab(response.json()) if response.status_code == requests.codes.ok else None