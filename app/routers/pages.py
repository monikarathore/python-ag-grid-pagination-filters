from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/", include_in_schema=False)
async def serve_employees_page():
    return FileResponse(os.path.join("static", "employees.html"))
