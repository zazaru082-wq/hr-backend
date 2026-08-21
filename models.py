from sqlalchemy import Column, Integer, String, Date, DateTime, Text, Float
from database import Base
import datetime

class Employee(Base):
    __tablename__ = "employees"
    person_id = Column(String, primary_key=True, index=True)
    title = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    nickname = Column(String)
    department = Column(String)
    position = Column(String)
    phone = Column(String)
    email = Column(String)
    status = Column(String)
    type = Column(String)

class Leave(Base):
    __tablename__ = "leaves"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    person_id = Column(String, index=True)
    leave_type = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    reason = Column(String)
    status = Column(String, default="รออนุมัติ")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Schedule(Base):
    __tablename__ = "schedules"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(Date)
    time = Column(String)
    title = Column(String)
    details = Column(String)
    location = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Project(Base):
    __tablename__ = "projects"
    project_id = Column(String, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text, nullable=True)
    department = Column(String, nullable=True)
    owner = Column(String, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    progress = Column(Integer, default=0)
    status = Column(String, default="กำลังดำเนินการ")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    doc_no = Column(String, unique=True, index=True)
    title = Column(String)
    category = Column(String)
    date = Column(Date)
    status = Column(String, default="ใช้งาน")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Rule(Base):
    __tablename__ = "rules"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category = Column(String)
    title = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Merit(Base):
    __tablename__ = "merits"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    person_id = Column(String, index=True)
    department = Column(String)
    date = Column(Date)
    activity = Column(String)
    hours = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Performance(Base):
    __tablename__ = "performances"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    person_id = Column(String, index=True)
    department = Column(String)
    topic = Column(String)
    activity = Column(String)
    date = Column(Date)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
