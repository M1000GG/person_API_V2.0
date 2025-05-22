from fastapi import APIRouter, Depends, HTTPException
from typing import List
from model.typedoc import Typedoc
from service.typedoc_service import TypedocService

typedoc_router = APIRouter(prefix="/typedocs", tags=["typedocs"])

# Will store the service that helps us manage document types
typedoc_service_instance: TypedocService = None

# Save the service to be used later in other parts of the api
def set_typedoc_service(service: TypedocService):
    global typedoc_service_instance
    typedoc_service_instance = service

# Provide the saved service when needed
def get_typedoc_service():
    return typedoc_service_instance

@typedoc_router.get("/", response_model=List[Typedoc])
def get_all_typedocs(service: TypedocService = Depends(get_typedoc_service)):
    # Get all available document types
    return service.get_all_typedocs()

@typedoc_router.get("/{code}", response_model=Typedoc)
def get_typedoc_by_code(code: int, service: TypedocService = Depends(get_typedoc_service)):
    # Get a specific document type by code
    typedoc = service.get_typedoc_by_code(code)
    if not typedoc:
        raise HTTPException(status_code=404, detail=f"Document type with code {code} not found")
    return typedoc

@typedoc_router.post("/", response_model=bool)
def create_typedoc(typedoc: Typedoc, service: TypedocService = Depends(get_typedoc_service)):
    # Create a new document type
    existing = service.get_typedoc_by_code(typedoc.code)
    if existing:
        raise HTTPException(status_code=409, detail=f"Document type with code {typedoc.code} already exists")

    return service.create_typedoc(typedoc)

@typedoc_router.put("/{code}", response_model=bool)
def update_typedoc(code: int, typedoc: Typedoc, service: TypedocService = Depends(get_typedoc_service)):
    # Update an existing document type
    existing = service.get_typedoc_by_code(code)
    if not existing:
        raise HTTPException(status_code=404, detail=f"Document type with code {code} not found")

    # Ensure the code in the path matches the code in the body
    if code != typedoc.code:
        raise HTTPException(status_code=400,
                            detail=f"Code in path ({code}) does not match code in body ({typedoc.code})")

    return service.update_typedoc(code, typedoc)

@typedoc_router.delete("/{code}", response_model=bool)
def delete_typedoc(code: int, service: TypedocService = Depends(get_typedoc_service)):
    # Delete a document type
    existing = service.get_typedoc_by_code(code)
    if not existing:
        raise HTTPException(status_code=404, detail=f"Document type with code {code} not found")

    return service.delete_typedoc(code)