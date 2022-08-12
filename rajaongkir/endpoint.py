"""Raja Ongkir API endpoints."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rajaongkir.client import BaseClient

class Endpoint:
    def __init__(self, base: "BaseClient") -> None:
        self.base = base


class ProvincesEndpoint(Endpoint):
    
    endpoint = 'province'
    def list(self):
        provinces = self.base.request(endpoint=ProvincesEndpoint.endpoint)
                
        self.base._status(provinces)

        return self.base._parse_response(provinces)

    def query(self, **kwargs):
        province = self.base.request(endpoint=ProvincesEndpoint.endpoint, params={'id': kwargs['province_id']})

        self.base._status(province)

        return self.base._parse_response(province)


class CitiesEndpoint(Endpoint):
    
    endpoint = 'city'
    
    def list(self):
        cities = self.base.request(endpoint=CitiesEndpoint.endpoint)
        
        self.base._status(cities)
        
        return self.base._parse_response(cities)
    
    def query(self, **kwargs):
        city = self.base.request(endpoint=CitiesEndpoint.endpoint, params={'id': kwargs.get('city_id'), 'province': kwargs.get('province_id')})
        

        self.base._status(city)

        return self.base._parse_response(city)


class CostEndpoint(Endpoint):
    def query(self, origin, destination, weight=0, courier=None):
        headers={
                'key': self.base.auth,
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'charset': 'utf8'
            }
        post_data = {
            "origin": origin,
            "destination": destination,
            "weight": int(weight),
            "courier": courier
        }
        response = self.base.request(endpoint = 'cost', headers=headers, pyload=post_data, method='post')
        self.base._status(response)
        return self.base._parse_response(response)
