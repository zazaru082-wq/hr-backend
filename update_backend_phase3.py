import os

with open('models.py', 'r', encoding='utf-8') as f:
    models_content = f.read()

if "class Schedule" not in models_content:
    models_content += """

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
"""
    with open('models.py', 'w', encoding='utf-8') as f:
        f.write(models_content)

with open('schemas.py', 'r', encoding='utf-8') as f:
    schemas_content = f.read()

if "class ScheduleBase" not in schemas_content:
    schemas_content += """

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
    department: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = "กำลังทำ"

class ProjectCreate(ProjectBase):
    project_id: str

class Project(ProjectBase):
    project_id: str
    class Config:
        orm_mode = True
"""
    with open('schemas.py', 'w', encoding='utf-8') as f:
        f.write(schemas_content)

with open('main.py', 'r', encoding='utf-8') as f:
    main_content = f.read()

if "/api/schedules" not in main_content:
    main_content += """

# ----- 03 คิวหัวหน้า (Schedules) -----
@app.post("/api/schedules/", response_model=schemas.Schedule)
def create_schedule(sched: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    db_sched = models.Schedule(**sched.dict())
    db.add(db_sched)
    db.commit()
    db.refresh(db_sched)
    return db_sched

@app.get("/api/schedules/", response_model=List[schemas.Schedule])
def read_schedules(db: Session = Depends(get_db)):
    return db.query(models.Schedule).order_by(models.Schedule.date.desc()).all()

# ----- 04 ผลงาน (Performances) -----
@app.post("/api/performances/", response_model=schemas.Performance)
def create_performance(perf: schemas.PerformanceCreate, db: Session = Depends(get_db)):
    db_perf = models.Performance(**perf.dict())
    db.add(db_perf)
    db.commit()
    db.refresh(db_perf)
    return db_perf

@app.get("/api/performances/", response_model=List[schemas.Performance])
def read_performances(db: Session = Depends(get_db)):
    return db.query(models.Performance).order_by(models.Performance.date.desc()).all()

# ----- 05 โครงการ (Projects) -----
@app.post("/api/projects/", response_model=schemas.Project)
def create_project(proj: schemas.ProjectCreate, db: Session = Depends(get_db)):
    db_proj = models.Project(**proj.dict())
    db.add(db_proj)
    db.commit()
    db.refresh(db_proj)
    return db_proj

@app.get("/api/projects/", response_model=List[schemas.Project])
def read_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()
"""
    with open('main.py', 'w', encoding='utf-8') as f:
        f.write(main_content)

print("Updated backend for Phase 3 (Menus 03, 04, 05)")
