from fastapi import APIRouter, Depends, HTTPException
from typing import List
from model.location import Location
from service.location_service import LocationService

location_router = APIRouter(prefix="/locations", tags=["locations"])

# Will store the service that helps us read and use location data
location_service_instance: LocationService = None

# Saves the service so be used later in other parts of the api
def set_location_service(service: LocationService):
    global location_service_instance
    location_service_instance = service

# Gives the saved service when we need it
def get_location_service():
    return location_service_instance

@location_router.get("/states", response_model=List[Location])
def get_states(service: LocationService = Depends(get_location_service)):
    return service.get_states()

@location_router.get("/by-state/{state_code}", response_model=List[Location])
def get_locations_by_state_code(state_code: int, service: LocationService = Depends(get_location_service)):
    return service.get_locations_by_state_code(state_code)

@location_router.get("/by-code/{code}", response_model=Location)
def get_location_by_code(code: int, service: LocationService = Depends(get_location_service)):
    location = service.get_location_by_code(code)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location

@location_router.get("/capitals", response_model=List[Location])
def get_capitals(service: LocationService = Depends(get_location_service)):
    return service.get_capitals()
