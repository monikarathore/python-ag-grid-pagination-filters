from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.models.employee import Employee
from app.models.employee_db import EmployeeDB
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.auth import verify_token
from sqlalchemy import asc, desc, or_, and_, func
import json
from app.utils.filters import build_filter_for_column

router = APIRouter()

@router.get("/employees-paginated", dependencies=[Depends(verify_token)])
async def get_employees_paginated(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
    sort_by: Optional[str] = Query("employee_id"),
    sort_order: Optional[str] = Query("asc"),
    filterModel: Optional[str] = Query(None),
):
    query = db.query(EmployeeDB)

    if filterModel:
        filters = json.loads(filterModel)
        conditions = []

        for col, filter_data in filters.items():
            column_attr = getattr(EmployeeDB, col, None)
            if not column_attr:
                continue
            if filter_data.get("filterType") == "text":
                cond = build_filter_for_column(column_attr, filter_data)
                conditions.append(cond)

        if conditions:
            query = query.filter(and_(*conditions))

    sort_column = getattr(EmployeeDB, sort_by, EmployeeDB.employee_id)
    sort_column = sort_column.asc() if sort_order == "asc" else sort_column.desc()
    query = query.order_by(sort_column)

    total = query.count()
    employees = query.offset((page - 1) * page_size).limit(page_size).all()

    return {
        "total": total,
        "data": [e.__dict__ for e in employees]
    }

@router.post("/employees/bulk", dependencies=[Depends(verify_token)])
async def create_employees_bulk(employees: List[Employee], db: Session = Depends(get_db)):
    # Collect employee_ids, emails, mobiles for validation
    employee_ids = [emp.employee_id for emp in employees]
    emails = [emp.email for emp in employees]
    mobiles = [emp.mobile for emp in employees]

    # Check for duplicates in DB for employee_id, email, or mobile
    existing_employees = db.query(EmployeeDB).filter(
        (EmployeeDB.employee_id.in_(employee_ids)) |
        (EmployeeDB.email.in_(emails)) |
        (EmployeeDB.mobile.in_(mobiles))
    ).all()

    if existing_employees:
        existing_details = [
            f"id:{e.employee_id}, email:{e.email}, mobile:{e.mobile}"
            for e in existing_employees
        ]
        raise HTTPException(
            status_code=400,
            detail=f"Employees already exist with these details: {existing_details}"
        )

    # Add all employees to DB
    db_employees = []
    for emp in employees:
        db_emp = EmployeeDB(
            employee_id=emp.employee_id,
            name=emp.name,
            salary=emp.salary,
            language=emp.language,
            email=emp.email,
            mobile=emp.mobile
        )
        db.add(db_emp)
        db_employees.append(db_emp)

    db.commit()
    # Refresh to get DB assigned fields if any
    for db_emp in db_employees:
        db.refresh(db_emp)

    return {"message": f"{len(db_employees)} employees created successfully", "employees": db_employees}

@router.post("/employee", dependencies=[Depends(verify_token)])
async def create_employee(employee: Employee, db: Session = Depends(get_db)):
    # Check if employee ID or email/mobile already exists
    existing = db.query(EmployeeDB).filter(
        (EmployeeDB.employee_id == employee.employee_id) |
        (EmployeeDB.email == employee.email) |
        (EmployeeDB.mobile == employee.mobile)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Employee ID or Email or Mobile already exists")

    db_employee = EmployeeDB(
        employee_id=employee.employee_id,
        name=employee.name,
        salary=employee.salary,
        language=employee.language,
        email=employee.email,
        mobile=employee.mobile
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return {"message": "Employee created successfully", "employee": db_employee}

@router.get("/employees", dependencies=[Depends(verify_token)])
async def get_all_employees(db: Session = Depends(get_db)):
    employees = db.query(EmployeeDB).all()
    return employees

@router.delete("/employees/clear", dependencies=[Depends(verify_token)])
async def clear_all_employees(db: Session = Depends(get_db)):
    db.query(EmployeeDB).delete()
    db.commit()
    return {"message": "All employees deleted successfully"}
