from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

class EmployeeBase(BaseModel):
    person_id: str
    title: str
    first_name: str
    last_name: str
    nickname: Optional[str] = None
    department: str
    position: str
    phone: Optional[str] = None
    email: Optional[str] = None
    status: str
    type: str

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    class Config:
        orm_mode = True

class LeaveBase(BaseModel):
    person_id: str
    leave_type: str
    start_date: date
    end_date: date
    reason: str
    status: Optional[str] = "รออนุมัติ"

class LeaveCreate(LeaveBase):
    pass

class Leave(LeaveBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

class ScheduleBase(BaseModel):
    date: date
    time: str
    title: str
    details: Optional[str] = None
    location: Optional[str] = None

class ScheduleCreate(ScheduleBase):
    pass

class Schedule(ScheduleBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    department: Optional[str] = None
    owner: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    progress: Optional[int] = 0
    status: Optional[str] = "กำลังดำเนินการ"

class ProjectCreate(ProjectBase):
    project_id: str

class Project(ProjectBase):
    project_id: str
    created_at: datetime
    class Config:
        orm_mode = True

class DocumentBase(BaseModel):
    doc_no: str
    title: str
    category: str
    date: date
    status: Optional[str] = "ใช้งาน"

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

class RuleBase(BaseModel):
    category: str
    title: str
    content: str

class RuleCreate(RuleBase):
    pass

class Rule(RuleBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

class MeritBase(BaseModel):
    person_id: str
    department: str
    date: date
    activity: str
    hours: float

class MeritCreate(MeritBase):
    pass

class Merit(MeritBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

class PerformanceBase(BaseModel):
    person_id: str
    department: str
    topic: str
    activity: str
    date: date
    image_url: Optional[str] = None

class PerformanceCreate(PerformanceBase):
    pass

class Performance(PerformanceBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True
