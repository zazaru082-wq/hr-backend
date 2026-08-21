import os

models_code = """
from sqlalchemy import Column, Integer, String, Date, Text, Boolean, DateTime
from database import Base
import datetime

class Employee(Base):
    __tablename__ = "employees"

    person_id = Column(String, primary_key=True, index=True) # P001
    status = Column(String) # สถานภาพ (พระ, อุบาสก, etc)
    gender = Column(String) # เพศ
    title = Column(String) # คำนำหน้า
    first_name = Column(String) # ชื่อ
    monastic_name = Column(String) # ฉายา
    last_name = Column(String) # นามสกุล
    dob = Column(Date, nullable=True) # วันเกิด
    age = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    phone = Column(String, nullable=True)
    line_id = Column(String, nullable=True)
    department = Column(String, nullable=True)
    date_joined = Column(Date, nullable=True)
    tenure = Column(String, nullable=True)
    secular_edu = Column(String, nullable=True)
    dhamma_edu = Column(String, nullable=True)
    temple_work_history = Column(Text, nullable=True)
    bank = Column(String, nullable=True)
    account_name = Column(String, nullable=True)
    account_number = Column(String, nullable=True)
    food_allergy = Column(String, nullable=True)
    drug_allergy = Column(String, nullable=True)
    disease = Column(String, nullable=True)
    other_health = Column(Text, nullable=True)
    photo_url = Column(String, nullable=True)
    note = Column(Text, nullable=True)
    last_updated = Column(Date, default=datetime.date.today)
"""

schemas_code = """
from pydantic import BaseModel
from typing import Optional
from datetime import date

class EmployeeBase(BaseModel):
    status: Optional[str] = None
    gender: Optional[str] = None
    title: Optional[str] = None
    first_name: Optional[str] = None
    monastic_name: Optional[str] = None
    last_name: Optional[str] = None
    dob: Optional[date] = None
    age: Optional[int] = None
    height: Optional[int] = None
    phone: Optional[str] = None
    line_id: Optional[str] = None
    department: Optional[str] = None
    date_joined: Optional[date] = None
    tenure: Optional[str] = None
    secular_edu: Optional[str] = None
    dhamma_edu: Optional[str] = None
    temple_work_history: Optional[str] = None
    bank: Optional[str] = None
    account_name: Optional[str] = None
    account_number: Optional[str] = None
    food_allergy: Optional[str] = None
    drug_allergy: Optional[str] = None
    disease: Optional[str] = None
    other_health: Optional[str] = None
    photo_url: Optional[str] = None
    note: Optional[str] = None

class EmployeeCreate(EmployeeBase):
    person_id: str

class EmployeeUpdate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    person_id: str
    last_updated: Optional[date] = None

    class Config:
        orm_mode = True
"""

main_code = """
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import models
import schemas
import datetime
from database import engine, get_db

models.Base.metadata.drop_all(bind=engine) # Drop old tables to rebuild with new schema
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Niramitsilp Fund API", version="2.0")

# Enable CORS for Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Niramitsilp Fund API"}

# ----- 01 บุคลากร (Employees) -----
@app.post("/api/employees/", response_model=schemas.Employee)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    db_emp = db.query(models.Employee).filter(models.Employee.person_id == employee.person_id).first()
    if db_emp:
        raise HTTPException(status_code=400, detail="Person ID already registered")
    
    new_emp = models.Employee(**employee.dict(), last_updated=datetime.date.today())
    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)
    return new_emp

@app.get("/api/employees/", response_model=List[schemas.Employee])
def read_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Employee).offset(skip).limit(limit).all()

@app.get("/api/employees/{person_id}", response_model=schemas.Employee)
def read_employee(person_id: str, db: Session = Depends(get_db)):
    db_emp = db.query(models.Employee).filter(models.Employee.person_id == person_id).first()
    if db_emp is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_emp

@app.put("/api/employees/{person_id}", response_model=schemas.Employee)
def update_employee(person_id: str, employee_update: schemas.EmployeeUpdate, db: Session = Depends(get_db)):
    db_emp = db.query(models.Employee).filter(models.Employee.person_id == person_id).first()
    if db_emp is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    update_data = employee_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_emp, key, value)
        
    db_emp.last_updated = datetime.date.today()
    db.commit()
    db.refresh(db_emp)
    return db_emp

@app.delete("/api/employees/{person_id}")
def delete_employee(person_id: str, db: Session = Depends(get_db)):
    db_emp = db.query(models.Employee).filter(models.Employee.person_id == person_id).first()
    if db_emp is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db.delete(db_emp)
    db.commit()
    return {"message": "Deleted successfully"}
"""

with open('models.py', 'w', encoding='utf-8') as f:
    f.write(models_code)
with open('schemas.py', 'w', encoding='utf-8') as f:
    f.write(schemas_code)
with open('main.py', 'w', encoding='utf-8') as f:
    f.write(main_code)
print("Updated FastAPI models, schemas, and main.py successfully!")
