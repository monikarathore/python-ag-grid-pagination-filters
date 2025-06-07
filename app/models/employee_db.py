from sqlalchemy import Column, Integer, String, Float
from app.db.database import Base

class EmployeeDB(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)  # internal DB PK
    employee_id = Column(Integer, unique=True, index=True, nullable=False)  # your unique employee id
    name = Column(String, nullable=False)
    salary = Column(Float, nullable=False)
    language = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    mobile = Column(String, unique=True, index=True, nullable=False)
