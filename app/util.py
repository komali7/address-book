
import sqlite3
from typing import Annotated
from app.model import Address
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from geopy.distance import geodesic


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
            print(geodesic((latitude, longitude), (addr_lat, addr_lon)).miles)
            if geodesic((latitude, longitude), (addr_lat, addr_lon)).miles <= distance:
                
                filtered_addresses.append(addr)
        return filtered_addresses
