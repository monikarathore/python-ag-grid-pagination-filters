from pydantic import BaseModel, EmailStr, Field, field_validator
import re

class Employee(BaseModel):
    employee_id: int = Field(..., example=1234)  # unique ID
    name: str = Field(..., example="Monika Thakur")
    salary: float = Field(..., gt=0, example=85000)
    language: str = Field(..., example="Python")
    email: EmailStr = Field(..., example="monika@example.com")
    mobile: str = Field(..., example="9876543210")

    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, mobile: str) -> str:
        pattern = r"^[6-9]\d{9}$"
        if not re.match(pattern, mobile):
            raise ValueError("Invalid mobile number")
        return mobile
