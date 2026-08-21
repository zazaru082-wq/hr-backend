
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


class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    person_id = Column(String, index=True) # ForeignKey could be used, but keeping simple
    leave_type = Column(String) # ลาป่วย, ลากิจ, ลาปฏิบัติธรรม
    start_date = Column(Date)
    end_date = Column(Date)
    reason = Column(Text, nullable=True)
    status = Column(String, default="รออนุมัติ") # รออนุมัติ, อนุมัติแล้ว, ไม่อนุมัติ
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Schedule(Base):
    __tablename__ = "schedules"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(Date)
    time_str = Column(String)
    topic = Column(String)
    location = Column(String)
    meal = Column(String, nullable=True) # ฉัน
    driver = Column(String, nullable=True)
    note = Column(Text, nullable=True)
    status = Column(String, default="กำลังดำเนินการ")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Performance(Base):
    __tablename__ = "performances"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    person_id = Column(String)
    project_id = Column(String, nullable=True)
    department = Column(String)
    topic = Column(String)
    activity = Column(String)
    detail = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    link_url = Column(String, nullable=True)
    date = Column(Date)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Project(Base):
    __tablename__ = "projects"
    project_id = Column(String, primary_key=True, index=True) # e.g. PJ-001
    name = Column(String)
    department = Column(String)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    status = Column(String, default="กำลังทำ")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    doc_id = Column(String, index=True) # D001
    category = Column(String)
    name = Column(String)
    link_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Rule(Base):
    __tablename__ = "rules"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    keyword = Column(String, index=True)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Merit(Base):
    __tablename__ = "merits"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)
    merit_type = Column(String) # งานบุญส่วนกลาง / บุคคล
    date = Column(Date)
    location = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
