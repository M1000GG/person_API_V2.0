from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from model.person import Person, PersonCreate, PersonUpdate
from model.location import Location
from model.typedoc import Typedoc
from service.person_service import PersonService
from service.location_service import LocationService
from service.typedoc_service import TypedocService

# Create the router for person endpoints
person_router = APIRouter(prefix="/persons", tags=["persons"])

# Store service instances (initially None)
person_service_instance: Optional[PersonService] = None
location_service_instance: Optional[LocationService] = None
typedoc_service_instance: Optional[TypedocService] = None


# Service configuration functions
def set_person_service(service: PersonService) -> None:
    """Store the person service instance"""
    global person_service_instance
    person_service_instance = service


def set_location_typedoc_services(
        location_service: LocationService,
        typedoc_service: TypedocService
) -> None:
    """Store location and typedoc service instances"""
    global location_service_instance, typedoc_service_instance
    location_service_instance = location_service
    typedoc_service_instance = typedoc_service


# Service getter functions with safety checks
def get_person_service() -> PersonService:
    """Get person service or raise error if not configured"""
    if person_service_instance is None:
        raise HTTPException(500, "Person service not configured")
    return person_service_instance


def get_location_service_for_persons() -> LocationService:
    """Get location service or raise error if not configured"""
    if location_service_instance is None:
        raise HTTPException(500, "Location service not configured")
    return location_service_instance


def get_typedoc_service_for_persons() -> TypedocService:
    """Get typedoc service or raise error if not configured"""
    if typedoc_service_instance is None:
        raise HTTPException(500, "Typedoc service not configured")
    return typedoc_service_instance


def _create_person_from_codes(
        person_create: PersonCreate,
        location_service: LocationService,
        typedoc_service: TypedocService
) -> Person:
    """Create Person object with auto-completed location and typedoc"""
    # Get location by code
    location = location_service.get_location_by_code(person_create.location_code)
    if not location:
        raise HTTPException(404, f"Location {person_create.location_code} not found")

    # Get typedoc by code
    typedoc = typedoc_service.get_typedoc_by_code(person_create.typedoc_code)
    if not typedoc:
        raise HTTPException(404, f"Document type {person_create.typedoc_code} not found")

    # Create complete Person object
    return Person(
        id=person_create.id,
        name=person_create.name,
        lastname=person_create.lastname,
        age=person_create.age,
        gender=person_create.gender,
        location=location,
        typedoc=typedoc
    )


def _create_person_from_update_codes(
        person_id: str,
        person_update: PersonUpdate,
        location_service: LocationService,
        typedoc_service: TypedocService
) -> Person:
    """Create Person object from PersonUpdate with auto-completed data"""
    # Get location by code
    location = location_service.get_location_by_code(person_update.location_code)
    if not location:
        raise HTTPException(404, f"Location {person_update.location_code} not found")

    # Get typedoc by code
    typedoc = typedoc_service.get_typedoc_by_code(person_update.typedoc_code)
    if not typedoc:
        raise HTTPException(404, f"Document type {person_update.typedoc_code} not found")

    # Create complete Person object
    return Person(
        id=person_id,  # Keep original ID
        name=person_update.name,
        lastname=person_update.lastname,
        age=person_update.age,
        gender=person_update.gender,
        location=location,
        typedoc=typedoc
    )


@person_router.post("/", response_model=bool)
def create_person(
        person_create: PersonCreate,
        parent_id: Optional[str] = None,
        person_service: PersonService = Depends(get_person_service),
        location_service: LocationService = Depends(get_location_service_for_persons),
        typedoc_service: TypedocService = Depends(get_typedoc_service_for_persons)
) -> bool:
    """Create a new person in the system using codes for location and typedoc"""

    # Check for duplicate ID
    if person_service.get_person_by_id(person_create.id):
        raise HTTPException(409, f"Person {person_create.id} already exists")

    # Check parent exists if provided
    if parent_id and not person_service.get_person_by_id(parent_id):
        raise HTTPException(404, f"Parent {parent_id} not found")

    # Create complete person object with auto-completed data
    person = _create_person_from_codes(person_create, location_service, typedoc_service)

    # Create the person
    if not person_service.create_person(person, parent_id):
        raise HTTPException(400, "Failed to create person")

    return True


@person_router.get("/", response_model=List[Person])
def get_all_persons(
        person_service: PersonService = Depends(get_person_service)
) -> List[Person]:
    """Get all persons in the system"""
    persons = person_service.get_all_persons()
    if not persons:
        raise HTTPException(404, "No persons found")
    return persons


@person_router.get("/{id}", response_model=Person)
def get_person_by_id(
        id: str,
        person_service: PersonService = Depends(get_person_service)
) -> Person:
    """Get a specific person by ID"""
    person = person_service.get_person_by_id(id)
    if not person:
        raise HTTPException(404, f"Person {id} not found")
    return person


@person_router.put("/{id}", response_model=bool)
def update_person(
        id: str,
        person_update: PersonUpdate,
        person_service: PersonService = Depends(get_person_service),
        location_service: LocationService = Depends(get_location_service_for_persons),
        typedoc_service: TypedocService = Depends(get_typedoc_service_for_persons)
) -> bool:
    """Update an existing person (ID and parent cannot be changed)"""
    # Check person exists
    if not person_service.get_person_by_id(id):
        raise HTTPException(404, f"Person {id} not found")

    # Create complete person object with auto-completed data
    person = _create_person_from_update_codes(id, person_update, location_service, typedoc_service)

    # Perform update
    if not person_service.update_person(id, person):
        raise HTTPException(400, f"Failed to update person {id}")

    return True


@person_router.delete("/{id}", response_model=bool)
def delete_person(
        id: str,
        person_service: PersonService = Depends(get_person_service)
) -> bool:
    """Delete a person from the system"""
    # Check person exists
    if not person_service.get_person_by_id(id):
        raise HTTPException(404, f"Person {id} not found")

    # Perform deletion
    if not person_service.delete_person(id):
        raise HTTPException(400, f"Cannot delete person {id}")

    return True


@person_router.get("/{id}/parent", response_model=Optional[Person])
def get_parent(
        id: str,
        person_service: PersonService = Depends(get_person_service)
):
    """Get direct parent of a person"""
    if not person_service.get_person_by_id(id):
        raise HTTPException(404, f"Person {id} not found")

    parent = person_service.get_parent(id)
    if not parent:
        raise HTTPException(404, f"No parent found for person {id}")
    return parent


@person_router.get("/{id}/children", response_model=List[Person])
def get_children(
        id: str,
        person_service: PersonService = Depends(get_person_service)
):
    """Get all children of a person"""
    if not person_service.get_person_by_id(id):
        raise HTTPException(404, f"Person {id} not found")

    children = person_service.get_children(id)
    if not children:
        raise HTTPException(404, f"No children found for person {id}")
    return children


@person_router.get("/filter/with-adult-children", response_model=List[Person])
def get_persons_with_adult_children(
        person_service: PersonService = Depends(get_person_service)
) -> List[Person]:
    """Get persons who have at least one adult child (18+)"""
    persons = person_service.get_persons_with_adult_child()
    if not persons:
        raise HTTPException(404, "No persons with adult children found")
    return persons


@person_router.get("/filter/by-criteria", response_model=List[Person])
def filter_persons(
        location_code: Optional[str] = Query(None, description="Location code filter"),
        typedoc_code: Optional[str] = Query(None, description="Document type code filter"),
        gender: Optional[str] = Query(None, description="Gender filter (M/F)"),
        person_service: PersonService = Depends(get_person_service)
) -> List[Person]:
    """Filter persons by multiple criteria"""
    # Require at least one filter
    if not any([location_code, typedoc_code, gender]):
        raise HTTPException(400, "At least one filter parameter required")

    # Validate gender format
    if gender and gender.upper() not in ["M", "F"]:
        raise HTTPException(400, "Gender must be 'M' or 'F'")

    # Get filtered results
    persons = person_service.filter_persons(location_code, typedoc_code, gender)
    if not persons:
        raise HTTPException(404, "No persons match the filters")

    return persons


@person_router.get("/filter/by-location/{location_code}", response_model=List[Person])
def get_persons_by_location(
        location_code: str,
        person_service: PersonService = Depends(get_person_service),
        location_service: LocationService = Depends(get_location_service_for_persons)
) -> List[Person]:
    """Get all persons from a specific location"""
    # Validate location exists
    if not location_service.get_location_by_code(int(location_code)):
        raise HTTPException(404, f"Location {location_code} not found")

    # Get persons by location
    persons = person_service.get_persons_by_location(location_code)
    if not persons:
        raise HTTPException(404, f"No persons found in location {location_code}")

    return persons