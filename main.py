from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from controller.location_controller import location_router, set_location_service
from controller.person_controller import person_router, set_person_service, set_location_typedoc_services
from controller.typedoc_controller import typedoc_router, set_typedoc_service
from service.location_service import LocationService
from service.person_service import PersonService
from service.typedoc_service import TypedocService

app = FastAPI()



# Create instances of services
location_service = LocationService("data/DIVIPOLA.csv")
typedoc_service = TypedocService()
person_service = PersonService()

# Set services for controllers
set_location_service(location_service)
set_typedoc_service(typedoc_service)
set_person_service(person_service)
set_location_typedoc_services(location_service, typedoc_service)

# Include routers
app.include_router(location_router)
app.include_router(typedoc_router)
app.include_router(person_router)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Log the error for debugging
    import traceback
    print(f"Exception occurred: {str(exc)}")
    print(traceback.format_exc())

    return JSONResponse(
        status_code=500,
        content={"message": f"Internal server error: {str(exc)}"}
    )


@app.get("/")
async def root():
    return {
        "message": "Person API V1",
        "endpoints": {
            "locations": "/locations",
            "typedocs": "/typedocs",
            "persons": "/persons"
        }
    }


# Run with: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)