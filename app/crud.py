# crud.py

from sqlalchemy.orm import Session
from .db.database import AddressModel
from .db.database import database
import requests
import configparser

# Create a ConfigParser object and read the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Access configuration values
api_key = config.get('API_KEY', 'API_KEY')
async def create_address(db: Session, address_data: dict):
    address_query = '+'.join(address_data['building_name'].split(" "))+'+'+'+'.join(address_data['street'].split(" "))+"+"+'+'.join(address_data['city'].split(" "))+'+'+'+'.join(address_data['state'].split(" "))+'+'+'+'.join(address_data['country'].split(" "))
    #url = f"https://api.geoapify.com/v1/geocode/search?street={street_name}&postcode={address_data['postal_code']}&city={address_data['city']}%2C%20Karnataka&state={address_data['state']}&format=json&apiKey=5c1d2a44b5d947059736a7423341c99a"
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address_query}&key={api_key}'

    response = requests.get(url)
    data = response.json()
    error_threshold=0.02
    lat_diff = abs(address_data['latitude'] - data['results'][0]['geometry']['location']['lat'])
    long_diff = abs(address_data['longitude'] - data['results'][0]['geometry']['location']['lng'])   
    if data['results'][0]['address_components'][-1]['long_name']!=address_data['postal_code']:
        return {'error': "The Postal Code is incorrect."}
    elif lat_diff <= error_threshold and long_diff <= error_threshold:
        query = AddressModel.__table__.insert().values(**address_data)
        address_id = await database.execute(query)
        return {'id':address_id}
    else:
        return {'error': "The Latitude and Longitude you provided does not correspond to the given address"}

async def get_addresses(db: Session, skip: int = 0, limit: int = 10):
    query = AddressModel.__table__.select().offset(skip).limit(limit)
    return await database.fetch_all(query)

async def get_address(db: Session, address_id: int):
    query = AddressModel.__table__.select().where(AddressModel.id == address_id)
    return await database.fetch_one(query)

async def update_address(db: Session, address_id: int, address_data: dict):
    query = AddressModel.__table__.update().where(AddressModel.id == address_id).values(**address_data)
    return await database.execute(query)

async def delete_address(db: Session, address_id: int):
    query = AddressModel.__table__.delete().where(AddressModel.id == address_id)
    return await database.execute(query)