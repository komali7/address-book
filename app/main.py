# main.py
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from geopy.distance import geodesic
import sqlite3

app = FastAPI()

# Database Initialization
conn = sqlite3.connect('addresses.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS addresses 
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             latitude REAL,
             longitude REAL,
             address TEXT)''')
conn.commit()


class Address(BaseModel):
    latitude: float
    longitude: float
    address: str


# Model
class AddressModel:
    @staticmethod
    def create_address(address: Address):
        conn = sqlite3.connect('addresses.db')
        c = conn.cursor()
        c.execute("INSERT INTO addresses (latitude, longitude, address) VALUES (?, ?, ?)",
                  (address.latitude, address.longitude, address.address))
        conn.commit()
        return c.lastrowid

    @staticmethod
    def update_address(address_id: int, address: Address):
        conn = sqlite3.connect('addresses.db')
        c = conn.cursor()
        c.execute("UPDATE addresses SET latitude = ?, longitude = ?, address = ? WHERE id = ?",
                  (address.latitude, address.longitude, address.address, address_id))
        conn.commit()

    @staticmethod
    def delete_address(address_id: int):
        conn = sqlite3.connect('addresses.db')
        c = conn.cursor()
        c.execute("DELETE FROM addresses WHERE id = ?", (address_id,))
        conn.commit()

    @staticmethod
    def get_address(address_id: int):
        conn = sqlite3.connect('addresses.db')
        c = conn.cursor()
        c.execute("SELECT * FROM addresses WHERE id = ?", (address_id,))
        return c.fetchone()

    @staticmethod
    def get_addresses_within_distance(latitude: float, longitude: float, distance: float):
        conn = sqlite3.connect('addresses.db')
        c = conn.cursor()
        c.execute("SELECT * FROM addresses")
        addresses = c.fetchall()
        filtered_addresses = []
        for addr in addresses:
            addr_lat, addr_lon, _ = addr[1:]
            if geodesic((latitude, longitude), (addr_lat, addr_lon)).miles <= distance:
                filtered_addresses.append(addr)
        return filtered_addresses


# Controller
@app.post("/addresses/", response_model=int)
def create_address(address: Address):
    address_id = AddressModel.create_address(address)
    return JSONResponse(content={"id": address_id})


@app.put("/addresses/{address_id}/")
def update_address(address_id: int, address: Address):
    AddressModel.update_address(address_id, address)
    return JSONResponse(content={"message": "Address updated successfully"})


@app.delete("/addresses/{address_id}/")
def delete_address(address_id: int):
    AddressModel.delete_address(address_id)
    return JSONResponse(content={"message": "Address deleted successfully"})


@app.get("/addresses/{address_id}/", response_model=Address)
def get_address(address_id: int):
    address_data = AddressModel.get_address(address_id)
    if address_data:
        return Address(latitude=address_data[1], longitude=address_data[2], address=address_data[3])
    else:
        return JSONResponse(content={"error": "Address not found"}, status_code=404)


@app.get("/addresses/", response_model=List[Address])
def get_addresses_within_distance(latitude: float, longitude: float, distance: float):
    addresses = AddressModel.get_addresses_within_distance(latitude, longitude, distance)
    return [
        {"latitude": addr[1], "longitude": addr[2], "address": addr[3]} for addr in addresses
    ]
