import unittest, os, sys

from unittest import TestCase
from dotenv import dotenv_values

current_dir = os.path.dirname(__file__)
base_dir = os.path.join(current_dir, os.pardir, os.pardir)
sys.path.append(base_dir)


from rajaongkir import Client


api_key = (dotenv_values('.env')['TOKEN'] if os.path.exists('.aa') else "04c24e424c1ff3be86283cec5982fd02")

class ApiRajaOngkirTests(TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.api = Client(api_key)
        super(ApiRajaOngkirTests, cls).setUpClass()
        
    def test_provinces(self):
        provinces = self.api.provinces.list()
        self.assertEqual(type(provinces), list)
    
    def test_provinces_query(self):
        province = self.api.provinces.query(province_id=9)
        self.assertEqual(type(province), dict)
    
    def test_cities(self):
        cities = self.api.cities.list()
        self.assertEqual(type(cities), list)
    
    def test_cities_query(self):
        city = {
            'city_id': 55, 'province_id': 9
        }
        city = self.api.cities.query(city_id = city['city_id'], province_id = city['province_id'])
        self.assertEqual(type(city), dict)
    
    def test_const_query(self):
        cost = self.api.cost.query(origin=55, destination=23, weight=1000, courier="jne")
        self.assertEqual(type(cost), list)


if __name__ == "__main__":
    unittest.main()
