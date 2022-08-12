## Raja Ongkir API

### API Documentation

`Raja Ongkir` is a RESTful API that provides the following services:

* **Object-Oriented Interface** - The API is implemented in object-oriented style.
* **Simple and Easy to Use** - The API is easy to use and simple to implement.

* **Province**: Get all province data
* **Province Detail**: Get province detail data
* **City**: Get all city data
* **Find City**: Get city data by province id
* **Cost**: Get all cost data
* **ETD**: Get all etd data
* **Varian Account Type**: Get all varian account type data

- [Raja Ongkir API Documentation](https://rajaongkir.com/docs/api)

---

## Installation

```bash
    pip install rajaongkir-py
```

## Usage

```python
    from rajaongkir import Client

    # Create a client object
    client = Client(auth='YOUR_API_KEY')
    
    # Get all province data
    provinces = client.provinces.list()

    # Get province detail data
    province = client.provinces.query(province_id=1)

    # Get all city data
    cities = client.cities.list()

    # Get city data by province id
    cities = client.cities.query(province_id=1)

    # Get ciry data by city id and province id
    city = client.cities.query(city_id=1, province_id=1)

    # Get calculate cost data
    cost = client.costs.calculate(origin=501, destination=114, weight=1000, courier='jne')
    
    # print cost data
    print(cost)

```
