from app.model import Address
from app.util import AddressModel
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from geopy.distance import geodesic
from loguru import logger

router = APIRouter()

@router.post("/addresses/", response_model=int)
def create_address(address: Address):
    try:
        address_id = AddressModel.create_address(address)
        logger.info(f"Address created successfully. : {address_id}")
        return JSONResponse(content={"id": address_id})
    except Exception as e:
        logger.error(f"Error creating address: {e}")
        return JSONResponse(content={"error": "An error occurred while creating the address"}, status_code=500)

@router.put("/addresses/{address_id}/")
def update_address(address_id: int, address: Address):
    try:
        AddressModel.update_address(address_id, address)
        logger.info(f"Address updated successfully. ID: {address_id}")
        return JSONResponse(content={"message": "Address updated successfully"})
    except Exception as e:
        logger.error(f"Error updating address with ID {address_id}: {e}")
        return JSONResponse(content={"error": "An error occurred while updating the address"}, status_code=500)

@router.delete("/addresses/{address_id}/")
def delete_address(address_id: int):
    try:
        AddressModel.delete_address(address_id)
        logger.info(f"Address deleted successfully. ID: {address_id}")
        return JSONResponse(content={"message": "Address deleted successfully"})
    except Exception as e:
        logger.error(f"Error deleting address with ID {address_id}: {e}")
        return JSONResponse(content={"error": "An error occurred while deleting the address"}, status_code=500)


@router.get("/addresses/{address_id}/", response_model=Address)
def get_address(address_id: int):
    try:
        address_data = AddressModel.get_address(address_id)
        if address_data:
            return Address(latitude=address_data[1], longitude=address_data[2], address=address_data[3])
        else:
            logger.warning(f"Address with ID {address_id} not found")
            return JSONResponse(content={"error": "Address not found"}, status_code=404)
    except Exception as e:
        logger.error(f"Error getting address with ID {address_id}: {e}")
        return JSONResponse(content={"error": "An error occurred while getting the address"}, status_code=500)


@router.get("/addresses/", response_model=List[Address])
def get_addresses_within_distance(latitude: float, longitude: float, distance: float):
    try:
        addresses = AddressModel.get_addresses_within_distance(latitude, longitude, distance)
        return [
            {"latitude": addr[1], "longitude": addr[2], "address": addr[3]} for addr in addresses
        ]
    except Exception as e:
        logger.error(f"Error getting addresses within distance: {e}")   
        return JSONResponse(content={"error": "An error occurred while getting addresses within distance"}, status_code=500)
