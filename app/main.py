from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.routers import employee, pages
from fastapi.staticfiles import StaticFiles
from app.db.database import engine, Base
import os
app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")),
    name="static"
)
app.include_router(pages.router)

# Include your employee router
app.include_router(employee.router)



# Create DB tables on startup
Base.metadata.create_all(bind=engine)

# Customize OpenAPI schema for Bearer token in Swagger UI (your existing code)
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Employee API",
        version="1.0.0",
        description="API with token-based authentication",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
