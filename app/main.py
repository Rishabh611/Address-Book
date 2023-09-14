from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .crud import create_address, get_addresses, get_address, update_address, delete_address
from .db.database import database
from .utils import haversine
app = FastAPI()

class AddressBase(BaseModel):
    flat_number: str
    building_name: str
    street: str
    city: str
    state: str
    postal_code: str
    country: str
    latitude: float
    longitude: float

class AddressCreate(AddressBase):
    pass

class AddressUpdate(AddressBase):
    pass

class LocationQuery(BaseModel):
    latitude: float
    longitude: float
    distance_km: float

class Address(AddressBase):
    id: int

    class Config:
        orm_mode = True

@app.on_event("startup")
async def startup_db_client():
    await database.connect()

@app.on_event("shutdown")
async def shutdown_db_client():
    await database.disconnect()

@app.post("/addresses/", response_model=Address)
async def create_new_address(address: AddressCreate):
    address_data = address.dict()
    data = await create_address(database, address_data)
    if 'error' in data:
        raise HTTPException(status_code=400, detail=data['error'])
    return {**address_data, "id": data['id']}

@app.get("/addresses/", response_model=list[Address])
async def get_address_list(skip: int = 0, limit: int = 10):
    return await get_addresses(database, skip, limit)

@app.get("/addresses/{address_id}", response_model=Address)
async def get_single_address(address_id: int):
    return await get_address(database, address_id)

@app.put("/addresses/{address_id}", response_model=Address)
async def update_single_address(address_id: int, address: AddressUpdate):
    address_data = address.dict()
    return await update_address(database, address_id, address_data)

@app.delete("/addresses/{address_id}", response_model=Address)
async def delete_single_address(address_id: int):
    return await delete_address(database, address_id)

@app.get("/retrieveAddresses/", response_model=list[Address])
async def get_addresses_nearby(location: LocationQuery):
    nearby_addresses = []
    addresses = await get_addresses(database)
    for address in addresses:
        distance = haversine(
            location.latitude, location.longitude,
            address["latitude"], address["longitude"]
        )
        if distance <= location.distance_km:
            nearby_addresses.append(address)

    return nearby_addresses