
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

from datetime import datetime

class LeaveRequestBase(BaseModel):
    person_id: str
    leave_type: str
    start_date: date
    end_date: date
    reason: Optional[str] = None
    status: Optional[str] = "รออนุมัติ"

class LeaveRequestCreate(LeaveRequestBase):
    pass

class LeaveRequest(LeaveRequestBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Schedule (เมนู 03)
class ScheduleBase(BaseModel):
    date: date
    time_str: str
    topic: str
    location: str
    meal: Optional[str] = None
    driver: Optional[str] = None
    note: Optional[str] = None
    status: Optional[str] = "กำลังดำเนินการ"

class ScheduleCreate(ScheduleBase):
    pass

class Schedule(ScheduleBase):
    id: int
    class Config:
        orm_mode = True

# Performance (เมนู 04)
class PerformanceBase(BaseModel):
    person_id: str
    project_id: Optional[str] = None
    department: str
    topic: str
    activity: str
    detail: Optional[str] = None
    image_url: Optional[str] = None
    link_url: Optional[str] = None
    date: date

class PerformanceCreate(PerformanceBase):
    pass

class Performance(PerformanceBase):
    id: int
    class Config:
        orm_mode = True

# Project (เมนู 05)
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    department: Optional[str] = None
    owner: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    progress: Optional[int] = 0
    status: Optional[str] = "กำลังทำ"

class ProjectCreate(ProjectBase):
    project_id: str

class Project(ProjectBase):
    project_id: str
    class Config:
        orm_mode = True


# Document (06)
class DocumentBase(BaseModel):
    doc_id: str
    category: str
    name: str
    link_url: Optional[str] = None

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int
    class Config:
        orm_mode = True

# Rule (07)
class RuleBase(BaseModel):
    keyword: str
    description: str

class RuleCreate(RuleBase):
    pass

class Rule(RuleBase):
    id: int
    class Config:
        orm_mode = True

# Merit (08)
class MeritBase(BaseModel):
    title: str
    merit_type: str
    date: date
    location: Optional[str] = None
    image_url: Optional[str] = None

class MeritCreate(MeritBase):
    pass

class Merit(MeritBase):
    id: int
    class Config:
        orm_mode = True
